with open('prototype.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    ('modalBiometricPrompt', 'Biometric Prompt Modal'),
    ('modalBiometricScan', 'Biometric Scan Modal'),
    ('handleBiometricScanClick', 'Biometric Scan Handler'),
    ('confirmActivateBiometrics', 'Biometric Confirm Handler'),
    ('linear-gradient(180deg, rgba(78, 10, 25, 0.90) 0%', 'Full Vinotinto Gradient on 100% of image'),
    ('bg-[#480C19]/45', 'Additional Vinotinto Layer'),
    ('gavelLoadingOverlay', '1.5s Gavel Loader'),
    ('eyeIconOpen', 'Minimalist Eye Open'),
    ('eyeIconClosed', 'Minimalist Eye Closed'),
]

print("--- VERIFYING PROTOTYPE FEATURES ---")
all_passed = True
for term, name in checks:
    if term in html:
        print(f"PASSED: {name}")
    else:
        print(f"FAILED: {name}")
        all_passed = False

if 'Acceso Rápido de Prueba' not in html:
    print("PASSED: 'Acceso Rápido de Prueba' successfully removed!")
else:
    print("FAILED: 'Acceso Rápido de Prueba' still present!")
    all_passed = False

if all_passed:
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
else:
    print("SOME TESTS FAILED")

