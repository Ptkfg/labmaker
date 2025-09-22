import pandas as pd
from app import db, EquipamentosTi, app
from datetime import datetime
import re

with app.app_context():
    df = pd.read_csv('data/cadastro_equipamentos_ti.csv', encoding='latin1', sep=',')

    print(df.columns)

    for _, row in df.iterrows():
        # Garantia
        garantia_str = str(row['Garantia'])
        garantia_num = re.findall(r'\d+', garantia_str)
        garantia = float(garantia_num[0]) if garantia_num else 0.0

        # corrigindo a Data de fabricação
        data_str = str(row['Data de fabricação']).strip()
        try:
            data_fabricacao = datetime.strptime(data_str, '%d/%m/%Y')
        except ValueError:
            data_fabricacao = None

        # Criar objeto
        equipamento = EquipamentosTi(
            nome=row['Nome'],
            garantia=garantia,
            fabricante_marca=row['Fabricante/marca '].strip(),
            modelo=row['Modelo '].strip(),
            numero_serie=row['Numero de serie '].strip(),
            data_fabricacao=data_fabricacao,
            validade=row['Validade '].strip().lower() in ['sim', 'true', '1'],
            condicao=row['Condição'],
            localizacao=row['Localização'],
            patrimonio=str(row['Patrimonio ']).strip(),
            quantidade=int(row['Quantidade']) if pd.notnull(row['Quantidade']) else 0
        )
        db.session.add(equipamento)

    db.session.commit()
    print('Dados importados com sucesso!')
