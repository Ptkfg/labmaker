from db import db
import os
import re
import sys
import pandas as pd
from datetime import datetime
from app import app
from models_equipamentos import NotasFiscais

CSV_PATH = os.path.join("data", "cadastro_notas_fiscais.csv")
ENCODING = "utf-8"
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
                descricaoes_itens = row.get("descricaoe_itens") or row.get("nome") or ""
                numero_nf = parse_int(row.get("numero_nf"), default=0)
                data_emissao = parse_date(row.get("Data de emissão") or row.get("Data de emissao") or row.get("Data de Emissão ") or "")
                fornecedor = (row.get("fornecedor ") or row.get("fornecedor") or row.get("Fornecedor") or "")
                cnpj = parse_float_from_text(row.get("CNPJ") or row.get("CNPJ") or "")
                quantidade = parse_int(row.get("Quantidade") or row.get("quantidade"), 0)
                valor_total= parse_float_from_text(row.get("Valor Total") or row.get("Valor Total") or "")



                item = NotasFiscais(
                    descricaoes_itens=str(descricaoes_itens).strip(),
                    numero_nf=str(numero_nf).strip(),
                    data_emissao=data_emissao,
                    fornecedor=str(fornecedor).strip(),
                    cnpj=cnpj,
                    valor_total=float(valor_total),
                    quantidade=quantidade
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