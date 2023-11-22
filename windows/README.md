# Build instructions for Windows
## Prerequisites
- Python

## Build

```powershell
cd windows
python .\setup.py bdist_msi 
```

## Launch

```powershell
cd windows\dist
.\Hamster-{version}-win64.msi
```