sayac = {}

with open("samples/kali_ssh_2026-11-18.log", "r", encoding="utf-8") as f:
    for line in f:
        if "Failed password" in line:
            parcalar = line.split()
            from_index = parcalar.index("from")
            ip = parcalar[from_index + 1]

            if ip not in sayac:
                sayac[ip] = 1
            else:
                sayac[ip] += 1

for ip, adet in sayac.items():
    print(f"{ip} -> {adet}")