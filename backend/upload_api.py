from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from datetime import datetime
from services.data_service import set_dataframe

router = APIRouter()

# ==========================================================
# Global Storage (Development)
# ==========================================================

uploaded_df = None


# ==========================================================
# Upload Excel
# ==========================================================

@router.post("/upload", tags=["Upload"])
async def upload_excel(file: UploadFile = File(...)):

    global uploaded_df

    # -----------------------------------
    # Validate File
    # -----------------------------------

    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(
            status_code=400,
            detail="Only Excel files (.xlsx, .xls) are allowed."
        )

    try:

        # -----------------------------------
        # Read Excel
        # -----------------------------------

        df = pd.read_excel(file.file)

        # Replace NaN values
        df = df.fillna("")

        # Convert to JSON-safe types
        df = df.astype(object)

        # Store in service layer (single source of truth)
        set_dataframe(df)

        # Keep legacy global in sync during migration
        uploaded_df = df

        # -----------------------------------
        # Console Output
        # -----------------------------------

        print("\n==========================================")
        print(" VisionIQ Excel Upload Successful")
        print("==========================================")
        print(f"Filename       : {file.filename}")
        print(f"Uploaded Time  : {datetime.now()}")
        print(f"Rows           : {len(df)}")
        print(f"Columns        : {len(df.columns)}")
        print("------------------------------------------")
        print(df.head())
        print("==========================================\n")

        # -----------------------------------
        # Response
        # -----------------------------------

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
            detail=f"Unable to read Excel file: {str(e)}"
        )


# ==========================================================
# Upload Status
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


# ==========================================================
# Return Entire Data (For Dashboard)
# ==========================================================

@router.get("/all-data", tags=["Upload"])
def all_data():

    global uploaded_df

    if uploaded_df is None:
        return []

    return uploaded_df.to_dict(orient="records")