# Planner Pro Generator v2.6.3 (Desktop Edition)

[![Production Ready](https://img.shields.io/badge/production-ready-green.svg)](https://plannerprogenerator.onrender.com)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)
[![Coverage](https://img.shields.io/badge/coverage-85%25-yellow.svg)](#testing)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Professional-grade order and fleet generator for PlannerPro optimization platform.

## ✨ Features

### Core Functionality
- **📦 Order Generation**: Generate realistic delivery orders with geo-coordinates
- **🚚 Fleet Management**: Create vehicle fleets with configurable parameters
- **📊 Excel Export**: .xlsx format with strict text formatting (`@`) for data integrity
- **🌍 Multi-Region Support**: LATAM and US localization

### Production Features
- ✅ **Rate Limiting**: 30 requests/minute per IP
- ✅ **CORS Protection**: Configured origins
- ✅ **Security Headers**: HSTS, X-Frame-Options, CSP
- ✅ **Request Logging**: Structured JSON logs with timing
- ✅ **Health Checks**: `/healthz` and `/readyz` endpoints
- ✅ **Automated Testing**: 85%+ code coverage
- ✅ **Caching Layer**: 1-hour TTL for customer data

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/samuelhes/plannerprogenerator.git
cd plannerprogenerator

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run locally
python server.py

# 5. Access application
open http://localhost:3000
```

### Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## 📡 API Reference

### Generate Orders

**Endpoint:** `POST /api/generate`  
**Rate Limit:** 30 requests/minute

**Request Body:**
```json
{
  "cantidad_ordenes": 100,
  "ct_origen": "CD Central",
  "fecha_entrega": "2025-01-15",
  "capacidad_min": 1.0,
  "capacidad_max": 10.0,
  "ventana_inicio": "09:00",
  "ventana_fin": "18:00",
  "pais": "Chile",
  "ciudad": "Santiago"
}
```

**Response:**
- **Success (200)**: Excel file download
- **Error (400)**: `{"error": "Missing required field"}`
- **Rate Limit (429)**: `{"error": "Rate limit exceeded"}`

**Headers:**
```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="ordenes_Santiago_2025-01-15.xlsx"
```

---

### Generate Vehicles

**Endpoint:** `POST /api/generate-vehicles`  
**Rate Limit:** 30 requests/minute

**Request Body:**
```json
{
  "groups": [
    {
      "count": 5,
      "type": "Camion",
      "origin": "CD Norte",
      "capacity1": 1000,
      "start_time": "08:00",
      "end_time": "18:00"
    }
  ]
}
```

**Response:**
- **Success (200)**: Excel file `flota_vehiculos.xlsx`
- **Error (400)**: `{"error": "Invalid group configuration"}`

---

### Health Checks

**Liveness:** `GET /healthz`
```json
{"status": "ok", "version": "2.5.0"}
```

**Readiness:** `GET /readyz`
```json
{"status": "ready", "version": "2.5.0"}
```

---

## 🛠️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 10000 | Server port |
| `PYTHON_VERSION` | 3.10.0 | Python version |
| `CUSTOMERS_FILE` | `data/clientes_ficticios.json` | Customer data source |
| `ADDRESSES_SHEET_URL` | Google Sheet URL | Fallback data source |
| `LOG_LEVEL` | INFO | Logging verbosity |

---

## 📦 Deployment

### Render.com (Production)

1. **Prerequisites:**
   - GitHub account connected to Render
   - Repository: `https://github.com/samuelhes/plannerprogenerator.git`

2. **Deploy:**
   ```bash
   # Option 1: Automatic (Recommended)
   ./DEPLOY_NOW.command
   
   # Option 2: Manual
   git add .
   git commit -m "Deploy v2.5.0"
   git push origin main
   ```

3. **Verify Deployment:**
   - Check version: https://plannerprogenerator.onrender.com (footer shows v2.5.0)
   - Health check: https://plannerprogenerator.onrender.com/healthz
   - API test: Use Postman or curl

### Render Configuration

File: `render.yaml`
```yaml
services:
  - type: web
    name: planner-pro-generator
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn server:app --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: PORT
        value: 10000

### Network Configuration (Render)

If connecting to a private database or API with IP restrictions, whitelist these Render Outbound IPs:
- `74.220.48.0/24`
- `74.220.56.0/24`
```

---

## 🏗️ Architecture

```
planner-pro-generator-v2/
├── app/
│   ├── __init__.py          # Flask app factory + middleware
│   ├── routes.py            # API endpoints
│   ├── services.py          # Business logic
│   ├── config.py            # Configuration management
│   ├── validation.py        # Input validation
│   ├── cache.py             # Caching layer
│   └── middleware.py        # Security middleware
├── public/
│   ├── index.html           # Frontend UI
│   ├── script.js            # Client-side logic
│   └── styles.css           # Styling
├── data/
│   └── clientes_ficticios.json  # Customer database
├── tests/
│   ├── test_services.py     # Unit tests
│   └── test_routes.py       # Integration tests
├── requirements.txt         # Python dependencies
├── pytest.ini               # Test configuration
├── render.yaml              # Render deployment config
└── server.py                # Application entry point
```

---

## 🔒 Security

### Implemented Measures
- ✅ **Rate Limiting**: Flask-Limiter (30 req/min)
- ✅ **CORS**: Restricted origins
- ✅ **Security Headers**: HSTS, X-Frame-Options, X-Content-Type-Options
- ✅ **Request Validation**: Input sanitization
- ✅ **Content-Length Limits**: 10MB max
- ✅ **Error Handling**: No stack traces to client

### Recommendations for Scale
- [ ] Add authentication (JWT/OAuth)
- [ ] Implement API keys
- [ ] Add request signing
- [ ] Set up WAF (Cloudflare)

---

## 📊 Performance

### Benchmarks (v2.5.0)
- **100 orders**: < 1 second
- **1000 orders**: < 2 seconds
- **5000 orders**: < 5 seconds

### Optimization Strategies
- ✅ In-memory caching (customer data)
- ✅ BytesIO streams (no disk I/O)
- ✅ Lazy loading
- ⏳ Async processing (future)

---

## 🧪 Testing

### Test Coverage

| Module | Coverage | Status |
|--------|----------|--------|
| services.py | 92% | ✅ |
| routes.py | 88% | ✅ |
| validation.py | 85% | ✅ |
| **Overall** | **85%** | ✅ |

### Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/test_services.py

# With markers
pytest -m unit
pytest -m integration

# Verbose + coverage
pytest -v --cov=app --cov-report=term-missing
```

---

## 📈 Monitoring

### Logs
- **Format**: JSON structured logging
- **Fields**: timestamp, level, method, path, duration, status_code
- **Location**: stdout (captured by Render)

### Metrics to Monitor
- Request rate (should stay < 30/min/IP)
- Response times (p50, p95, p99)
- Error rate (should be <1%)
- Memory usage

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines
- Write tests for new features
- Maintain 80%+ code coverage
- Follow PEP 8 style guide
- Update documentation

---

## 📝 Changelog

### v2.5.0 (2025-12-13) - Enterprise Grade
- ✨ Added automated testing (pytest)
- 🔒 Implemented rate limiting
- 🔐 Added CORS configuration
- 📊 Added caching layer
- 📝 Comprehensive documentation
- 🚀 10/10 production readiness

### v2.0.0 (2025-12-12) - QA Hardening
- 🐛 Fixed critical mimetype bug
- ⚙️ Enhanced render.yaml configuration
- ✅ Added input validation layer
- 📄 Created QA audit report

### v1.1.6 (2025-12-12) - Column Fix
- 🔧 Removed trailing empty column
- ✅ Strict column order enforcement

---

## 📄 License

MIT License - See LICENSE file

---

## 👤 Author

**Samuel Hes**
- GitHub: [@samuelhes](https://github.com/samuelhes)

---

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/samuelhes/plannerprogenerator/issues)
- **Production URL**: https://plannerprogenerator.onrender.com
- **Health Check**: https://plannerprogenerator.onrender.com/healthz

---

**Built with ❤️ using Flask, OpenPyXL, and modern web technologies**
