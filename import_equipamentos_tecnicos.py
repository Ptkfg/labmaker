from db import db
import os
import re
import sys
import pandas as pd
from datetime import datetime
from app import app
from models_equipamentos import EquipamentosTecnicos

CSV_PATH = os.path.join("data", "cadastro_equipamentos_tecnicos.csv")
ENCODING = "latin1"
SEP = ","


def parse_int(v, default=0):
    try:
        if pd.isna(v):
            return default
        return int(float(str(v).strip()))
    except Exception:
        return default


def parse_float_from_text(v, default=0.0):
    try:
        if pd.isna(v):
            return default
        s = str(v)
        nums = re.findall(r"[-+]?\d+[.,]?\d*", s)
        if not nums:
            return default
        n = nums[0].replace(",", ".")
        return float(n)
    except Exception:
        return default


def parse_date(v):
    if pd.isna(v):
        return None
    s = str(v).strip()
    if not s:
        return None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None


def normalize_colname(name):
    return re.sub(r"\s+", " ", str(name)).strip()


def load_df(path):
    try:
        df = pd.read_csv(path, encoding=ENCODING, sep=SEP)
        df.columns = [normalize_colname(c) for c in df.columns]
        return df
    except FileNotFoundError:
        print("Arquivo CSV não encontrado:", path, file=sys.stderr)
        raise
    except Exception as e:
        print("Erro lendo CSV:", repr(e), file=sys.stderr)
        raise


def import_rows(df, batch_size=200):
    inserted = 0
    with app.app_context():
        db.create_all()
        try:
            for i, row in df.iterrows():
                nome = row.get("Nome") or row.get("nome") or ""
                garantia = parse_float_from_text(row.get("Garantia") or row.get("Garantia ") or "")
                fabricante = (row.get("Fabricante/marca ") or row.get("Fabricante/marca") or row.get("Fabricante") or "")
                modelo = (row.get("Modelo ") or row.get("Modelo") or "")
                numero_serie = str(row.get("Numero de serie ") or row.get("Numero de serie") or row.get("Número de série") or "").strip()
                data_fabricacao = parse_date(row.get("Data de fabricação") or row.get("Data de fabricacao") or row.get("Data de fabricação ") or "")
                validade = str(row.get("Validade ") or row.get("Validade") or "").strip().lower() in ("sim", "true", "1", "yes")
                condicao = row.get("Condição") or row.get("Condicao") or ""
                localizacao = row.get("Localização") or row.get("Localizacao") or ""
                patrimonio = str(row.get("Patrimonio ") or row.get("Patrimonio") or "").strip()
                quantidade = parse_int(row.get("Quantidade") or row.get("quantidade"), 0)

                item = EquipamentosTecnicos(
                    nome=str(nome).strip(),
                    garantia=garantia,
                    fabricante_marca=str(fabricante).strip(),
                    modelo=str(modelo).strip(),
                    numero_serie=numero_serie,
                    data_fabricacao=data_fabricacao,
                    validade=validade,
                    condicao=str(condicao),
                    localizacao=str(localizacao),
                    patrimonio=patrimonio,
                    quantidade=quantidade,
                )
                db.session.add(item)
                inserted += 1

                if inserted % batch_size == 0:
                    db.session.commit()
            db.session.commit()
            print("Import concluído. Registros adicionados:", inserted)
        except Exception as e:
            db.session.rollback()
            print("Erro durante a importação:", repr(e), file=sys.stderr)
            raise


if __name__ == "__main__":
    df = load_df(CSV_PATH)
    import_rows(df)
