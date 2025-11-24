Write-Host "Testing YarnGPT CLI..." -ForegroundColor Green

Write-Host "`n1. Testing help commands..." -ForegroundColor Yellow
yarngpt --help
yarngpt version
yarngpt info

Write-Host "`n2. Testing conversion..." -ForegroundColor Yellow
yarngpt convert "Hello Nigeria" -o test1.mp3

Write-Host "`n3. Testing voices..." -ForegroundColor Yellow
yarngpt convert "Testing Emma" --voice emma -o test2.mp3

Write-Host "`n4. Testing formats..." -ForegroundColor Yellow
yarngpt convert "WAV test" --format wav -o test3.wav

Write-Host "`n5. Testing batch..." -ForegroundColor Yellow
"Hello", "Welcome", "Goodbye" | Out-File batch_test.txt -Encoding UTF8
yarngpt batch batch_test.txt -o batch_output

Write-Host "`nAll tests completed!" -ForegroundColor Green
Get-ChildItem *.mp3, *.wav
Get-ChildItem batch_output -ErrorAction SilentlyContinue