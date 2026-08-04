from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from datetime import datetime

router = APIRouter()

# ==========================================================
# Global Data Storage
# ==========================================================

uploaded_df = None

# ==========================================================
# Upload Excel
# ==========================================================

@router.post("/upload", tags=["Upload"])
async def upload_excel(file: UploadFile = File(...)):

    global uploaded_df

    # ---------------------------------------
    # Validate file
    # ---------------------------------------

    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400,
            detail="Only Excel files (.xlsx, .xls) are allowed."
        )

    try:

        # ---------------------------------------
        # Read Excel
        # ---------------------------------------

        df = pd.read_excel(file.file)

        # Replace NaN
        df = df.fillna("")

        # Convert values to JSON-safe types
        df = df.astype(object)

        # Store globally
        uploaded_df = df

        # ---------------------------------------
        # Console Log
        # ---------------------------------------

        print("\n========================================")
        print("📂 VisionIQ Excel Upload Successful")
        print("========================================")
        print(f"Filename      : {file.filename}")
        print(f"Rows          : {len(df)}")
        print(f"Columns       : {len(df.columns)}")
        print(f"Uploaded Time : {datetime.now()}")
        print("----------------------------------------")
        print(df.head())
        print("========================================\n")

        # ---------------------------------------
        # Response
        # ---------------------------------------

        return {

            "success": True,

            "message": "Excel uploaded successfully.",

            "filename": file.filename,

            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "rows": len(df),

            "columns": list(df.columns),

            "column_count": len(df.columns),

            "preview": df.head(20).to_dict(orient="records"),

            "dtypes": {
                col: str(dtype)
                for col, dtype in df.dtypes.items()
            }

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to read Excel file : {str(e)}"
        )


# ==========================================================
# Uploaded Data Information
# ==========================================================

@router.get("/uploaded-data-info", tags=["Upload"])
def uploaded_data_info():

    global uploaded_df

    if uploaded_df is None:

        return {

            "uploaded": False,

            "message": "No Excel file uploaded."

        }

    return {

        "uploaded": True,

        "rows": len(uploaded_df),

        "columns": list(uploaded_df.columns),

        "column_count": len(uploaded_df.columns)

    }


# ==========================================================
# Preview Uploaded Data
# ==========================================================

@router.get("/preview", tags=["Upload"])
def preview():

    global uploaded_df

    if uploaded_df is None:
        return []

    return uploaded_df.head(20).to_dict(orient="records")