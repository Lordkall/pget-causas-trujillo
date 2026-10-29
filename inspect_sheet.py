import sys
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SERVICE_ACCOUNT_FILE = 'credentials.json'
SPREADSHEET_ID = '1v2tCFT_JhXwjzX_hlRbR7PisfR4W-Y4IXQ0SgMrP9xg'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    print("=" * 60)
    print("VERIFICANDO CONEXION CON GOOGLE SHEETS...")
    print("=" * 60)
    
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        print(f"Credenciales cargadas: {creds.service_account_email}")
        
        service = build('sheets', 'v4', credentials=creds)
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        
        title = sheet_metadata.get('properties', {}).get('title')
        print(f"Conexion EXITOSA a la hoja: '{title}'")
        
        sheets = sheet_metadata.get('sheets', [])
        print(f"Pestanas encontradas ({len(sheets)}):")
        for s in sheets:
            p = s.get('properties', {})
            sheet_id = p.get('sheetId')
            sheet_title = p.get('title')
            print(f"   * {sheet_title} (gid: {sheet_id})")
            
            # Read first rows to see existing headers!
            result = service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=f"'{sheet_title}'!A1:Z5"
            ).execute()
            rows = result.get('values', [])
            if rows:
                print(f"     Filas encontradas:")
                for i, r in enumerate(rows):
                    print(f"       Fila {i+1}: {r}")
            else:
                print("     (Pestana vacia)")
                
    except HttpError as err:
        if err.resp.status == 403:
            print("\nERROR 403: Permiso Denegado")
            print("Debes compartir la hoja de calculo con la cuenta de servicio:")
            print(f"Correo: dataasuntosj@data-asuntos-juridicos.iam.gserviceaccount.com")
            print("Rol: Editor")
        else:
            print(f"\nError HTTP: {err}")
    except Exception as e:
        print(f"\nError inesperado: {e}")

if __name__ == '__main__':
    main()
