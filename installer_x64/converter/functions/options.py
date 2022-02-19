import pandas as pd

# Option 1: Add an "A" at the end of each line of the file selected
def process_1(file_name):
    with open(file_name, "r") as file:
        data = file.readlines()
    stripped_data = []
    for line in data:
        stripped_data.append(line.strip() + "A" + "\n")
    return stripped_data

###################################################################################################################

# Option 2: Convert the csv file of retentions from AGIP into a txt for importing to SIFERE
def process_2(file_name):
    # Sometime thw downloaded file has a first line that must be removed in order to the rest of the program work
    with open(file_name, 'r') as f:
        lines = f.readlines()
        if '=' in lines[0]:
            lines.pop(0)

    with open(file_name, 'w') as f:
        for line in lines:
            f.write(line)

    # Read the csv file and create a DF
    ret_df = pd.DataFrame(pd.read_csv(file_name, index_col=False, sep=","))

    #Delete retentions fields are not numbers
    control_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", "-"]
    for n in ret_df["Monto Retenido"]:
        for character in n:
            if character not in control_characters:
                invalid_character = n
                ret_df = ret_df[ret_df["Monto Retenido"] != invalid_character]
                ret_df.reset_index(drop=True, inplace=True)

    # Convert DF columns into necessary format
    for column in ret_df.columns:
        ret_df[column] = ret_df[column].astype(str)

    ret_df["N° Ader"] = ret_df["N° Ader"].apply(lambda x: "0" + str(x))
    ret_df["Tipo Comprobante"] = ret_df["Tipo Comprobante"].apply(
        lambda x: x.replace("X", "O").replace("L", "O").replace("R", "O"))
    ret_df["N° Comprobante"] = ret_df["N° Comprobante"].apply(
        lambda x: x.zfill(16).replace(" ", "0").replace("A", "0"))
    ret_df["N° Certificado"] = ret_df["N° Certificado"].apply(
        lambda x: x.replace("-", "").replace("ORDD", "").zfill(20))
    ret_df["Monto Retenido"] = ret_df["Monto Retenido"].apply(
        lambda x: x.replace(".", ","))

    # Build the fields for txt
    jurisdiction = "90100"
    cuit = ret_df["CUIT"]
    date = ret_df["Fecha Retencion"]
    succursal = ret_df["N° Ader"].str[-4:]
    bill_number = ret_df["N° Comprobante"].str[-16:]
    bill_type = ret_df["Tipo Comprobante"]
    bill_letter = "A"
    certificate = ret_df["N° Certificado"]
    retention = ret_df["Monto Retenido"]

    # After create retention field iterate and split de values to add 00 at the end
    decimals = []
    for i in range(len(retention)):
        decimals.append(retention[i].split(","))
        for j in range(len(decimals)):
            if len(decimals[j][1]) < 2:
                decimals[j][1] = decimals[j][1] + "0"
    for i in range(len(decimals)):
        retention[i] = (",".join(decimals[i]).zfill(11))

    # Create th final string with all the info
    data = jurisdiction + cuit + date + succursal + bill_number + \
        bill_type + bill_letter + certificate + retention

    # Concatenate fields for txt
    txt = []
    for line in data:
        txt.append(line + "\n")
    return txt

############################################################################################################################

# Option 3: Convert the csv file of perceptions from AGIP into a txt for importing to SIFERE
def process_3(file_name):
    # Sometime thw downloaded file has a first line that must be removed in order to the rest of the program work
    with open(file_name, 'r') as f:
        lines = f.readlines()
        if '=' in lines[0]:
            lines.pop(0)

    with open(file_name, 'w') as f:
        for line in lines:
            f.write(line)

    # Read the csv file and create a DF
    percep_df = pd.DataFrame(pd.read_csv(
        file_name, index_col=False))

    # Convert DF columns into necessary format
    for column in percep_df.columns:
        percep_df[column] = percep_df[column].astype(str)

    percep_df["N° Ader"] = percep_df["N° Ader"].apply(lambda x: "0" + str(x))
    percep_df["Tipo Comprobante"] = percep_df["Tipo Comprobante"].apply(
        lambda x: x.replace("X", "O").replace("L", "O").replace("R", "O"))
    percep_df["N° Comprobante"] = percep_df["N° Comprobante"].apply(
        lambda x: x.zfill(8).replace(" ", "0").replace("A", "0"))
    percep_df["Monto Percibido"] = percep_df["Monto Percibido"].apply(
        lambda x: x.replace(".", ","))

    # Build the fields for txt
    jurisdiction = "90100"
    cuit = percep_df["CUIT"]
    date = percep_df["Fecha Percepcion"]
    succursal = percep_df["N° Ader"].str[-4:]
    bill_number = percep_df["N° Comprobante"].str[-8:]
    bill_type = percep_df["Tipo Comprobante"]
    bill_letter = "A"
    perception = percep_df["Monto Percibido"]

    # After create perception field iterate and split de values to add 00 at the end
    decimals = []
    for i in range(len(perception)):
        decimals.append(perception[i].split(","))
        for j in range(len(decimals)):
            if len(decimals[j][1]) < 2:
                decimals[j][1] = decimals[j][1] + "0"
    for i in range(len(decimals)):
        perception[i] = (",".join(decimals[i]).zfill(11))

    # Create th final string with all the info
    data = jurisdiction + cuit + date + succursal + bill_number + \
        bill_type + bill_letter + perception

    # Concatenate fields for txt
    txt = []
    for line in data:
        txt.append(line + "\n")
    return txt

###############################################################################################################

# Option 4: Convert a excel file from Misiones web into two txt files for import into Misisones web
def process_4_1(file_name):
    # Read file
    df = pd.read_excel(file_name)

    # Create a df for retentions and perceptions
    ret_df = pd.DataFrame(df[df["Origen"] == "Compras"])
    percep_df = pd.DataFrame(df[df["Origen"] == "Ventas"])

    # Convert DF columns into necessary format
    for column in ret_df.columns:
        ret_df[column] = ret_df[column].astype(str)
    for column in ret_df.columns:
        percep_df[column] = percep_df[column].astype(str)
    ret_df["Fecha ret/per"] = ret_df["Fecha ret/per"].apply(
        lambda x: x.replace("/", "-"))

    # Build all the fields for txt
    date = ret_df["Fecha ret/per"].str[:10]
    bill_number = ret_df["Nro. de comprobante"].str[-9:]
    name = ret_df["Razon social"]
    id = ret_df["Nro. documento"]
    amount = ret_df["Monto sujeto retención"]
    percentage = ret_df["Alicuota IB"]
    data = date + "," + bill_number + "," + name + \
        ", ," + id + "," + amount + "," + percentage

    # Concatenate fields for txt
    txt = []
    for line in data:
        txt.append(line + '\n')
    return txt


def process_4_2(file_name):
    # Read file
    df = pd.read_excel(file_name)

    # Create a df for retentions and perceptions
    ret_df = pd.DataFrame(df[df["Origen"] == "Compras"])
    percep_df = pd.DataFrame(df[df["Origen"] == "Ventas"])

    # Convert DF columns into necessary format
    for column in ret_df.columns:
        ret_df[column] = ret_df[column].astype(str)
    for column in ret_df.columns:
        percep_df[column] = percep_df[column].astype(str)
    ret_df["Fecha ret/per"] = ret_df["Fecha ret/per"].apply(
        lambda x: x.replace("/", "-"))

    # Build all the fields for txt
    date = percep_df["Fecha ret/per"].str[:10]
    bill_type = percep_df["Tipo"].str[:2] + \
        "_" + percep_df["Nro. de comprobante"].str[:1]
    bill_number = percep_df["Nro. de comprobante"].str[-9:]
    name = percep_df["Razon social"]
    id = percep_df["Nro. documento"]
    amount = percep_df["Monto sujeto retención"]
    percentage = percep_df["Alicuota IB"]
    data = date + "," + bill_type + "," + bill_number + "," + name + \
        "," + id + "," + amount + "," + percentage

    # Concatenate fields for txt
    txt = []
    for line in data:
        txt.append(line + '\n')
    return txt