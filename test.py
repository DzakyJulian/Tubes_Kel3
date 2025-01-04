email = "jonas@gmail.com"
e_arr = []
atsym_count = 0
atsym_idx = 0
is_valid = None

for i in range(len(email)):
    e_arr.append(email[i])
    
print(e_arr)
print(len(e_arr))

# Check apakah ada symbol @?
for i in range(len(e_arr)):
    if e_arr[i] == "@":
        atsym_count += 1
        atsym_idx = i if atsym_count <= 1 else None
    else:
        if i == (len(e_arr) - 1):
            is_valid = False
            break
        else:
            continue
print(f"Index @: {atsym_idx}")

# Check apakah ada domain name?
# for i in range(len(e_arr)):
    

if atsym_count > 1:
    is_valid = False
    
if atsym_count == 1:
    is_valid = True
    
print("Email valid." if is_valid else "Email tidak valid.")