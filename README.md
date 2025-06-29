# Data Extraction Repository

This repository contains extracted data from various sources for analysis and research purposes.

## Contents

### Customer Data
- **File**: `all_customers_complete.json`
- **Records**: 63,722 customer records
- **Size**: 34MB
- **Format**: JSON

#### Sample Customer Record
```json
{
  "id": 1,
  "name": "Customer Name",
  "email": "customer@example.com",
  "is_corporate": false,
  "is_active": true,
  "is_fraud": false,
  "tc_kimlik_no": "12345678901",
  "tax_no": "1234567890",
  "city": "Istanbul",
  "country": "Turkey",
  "created_at": "13.04.2022 00:45:31",
  "source": "erp",
  "price_group": null,
  "customer_group": null,
  "segment": null,
  "external_id": "EXT123",
  "integration_external_id": null
}
```

#### Data Fields
- **Personal Info**: name, email, tc_kimlik_no, tax_no
- **Business Info**: is_corporate, customer_group, price_group
- **Location**: city, country
- **Status**: is_active, is_fraud, is_cancelled
- **Metadata**: created_at, source, segment, external_id

### Documents (Excel Reports)
- **Location**: `docs/` folder
- **Count**: 14 files downloaded
- **Total Size**: ~8.6MB
- **Formats**: .xls files

#### Available Reports
- Customer lists: `customer_list_2025-06-29_23-58-41.xls` (6.8MB)
- Invoice reports: Multiple `invoice_list_*.xls` files
- Sales details: `selling_orders_details_2025-02-20_16-46-57.xls`
- Monthly reports: `MAYIS_2025-06-02_14-39-31.xls`
- Custom reports: Various dated reports

## Data Statistics

### Customer Demographics
- **Total Customers**: 63,722
- **Corporate vs Individual**: Mixed customer base
- **Geographic Distribution**: Turkey-focused
- **Data Sources**: ERP systems, Trendyol marketplace

### Data Quality
- Complete records with minimal null values
- Structured format with consistent field naming
- Temporal data spanning 2022-2025
- Multiple integration sources tracked

## Technical Details

### Extraction Method
- API endpoints accessed via authenticated POST requests
- DataTables pagination handled automatically
- Batch processing for large datasets (1000 records/request)
- Amazon S3 document downloads with session authentication

### Data Processing
- JSON formatting and validation
- Unicode character handling
- File compression and optimization
- Error handling for failed downloads

## File Structure
```
├── all_customers_complete.json          # Complete customer database
├── customer_data_formatted.json         # Sample/test data
├── documents_response.json              # Document metadata
├── docs/                               # Downloaded Excel reports
│   ├── customer_list_*.xls
│   ├── invoice_list_*.xls
│   └── [various reports]
├── fetch_all_customers.py              # Customer extraction script
├── download_with_auth.py               # Document download script
└── README.md                           # This file
```

## Usage Notes

- All data extracted for research and analysis purposes
- Customer information includes sensitive PII - handle appropriately
- Excel reports contain business intelligence data
- Timestamps indicate data collection period: 2022-2025

## Data Sources

1. **Customer API**: `/customer/list/search/`
   - Pagination: 1000 records per request
   - Authentication: Session-based
   - Format: JSON response

2. **Document API**: `/document/list/json/`
   - File storage: Amazon S3 (EU-West-1)
   - Access: Authenticated download links
   - Formats: Excel (.xls) reports

---

*Last Updated: June 29, 2025*
*Repository: Anonymous data extraction project*