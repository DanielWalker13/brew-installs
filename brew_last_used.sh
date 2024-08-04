
#!/bin/bash

brew_prefix=$(brew --prefix)
current_time=$(date +%s)
six_months_ago=$((current_time - 15552000)) # 6 months in seconds

# Function to format the date
format_date() {
    date -r $1 +"%b %d %Y"
}

# Function to get the length of the longest package name
get_max_pkg_length() {
    max_length=0
    for pkg in $(brew list); do
        length=${#pkg}
        if (( length > max_length )); then
            max_length=$length
        fi
    done
    echo $max_length
}

max_pkg_length=$(get_max_pkg_length)

# Check for the flag
print_old_only=false
if [[ $1 == "--old-only" ]]; then
    print_old_only=true
fi

# Iterate through each package and find the last access time
for pkg in $(brew list); do
    last_access=$(find "$brew_prefix/Cellar/$pkg" -type f -exec stat -f '%a' {} + 2>/dev/null | sort -n | tail -1)
    if [[ -n "$last_access" ]]; then
        if [[ "$print_old_only" == false || "$last_access" -lt "$six_months_ago" ]]; then
            formatted_date=$(format_date $last_access)
            printf "%-${max_pkg_length}s was last accessed on: %s\n" "$pkg" "$formatted_date"
        fi
    else
        printf "%-${max_pkg_length}s has no recorded access time\n" "$pkg"
    fi
done


# #!/bin/bash

# brew_prefix=$(brew --prefix)

# # Function to format the date
# format_date() {
#     date -r $1 +"%b %d %Y"
# }

# # Function to get the length of the longest package name
# get_max_pkg_length() {
#     max_length=0
#     for pkg in $(brew list); do
#         length=${#pkg}
#         if (( length > max_length )); then
#             max_length=$length
#         fi
#     done
#     echo $max_length
# }

# max_pkg_length=$(get_max_pkg_length)

# # Iterate through each package and find the last access time
# for pkg in $(brew list); do
#     last_access=$(find "$brew_prefix/Cellar/$pkg" -type f -exec stat -f '%a' {} + 2>/dev/null | sort -n | tail -1)
#     if [[ -n "$last_access" ]]; then
#         formatted_date=$(format_date $last_access)
#         printf "%-${max_pkg_length}s was last accessed on: %s\n" "$pkg" "$formatted_date"
#     else
#         printf "%-${max_pkg_length}s has no recorded access time\n" "$pkg"
#     fi
# done

# # #!/bin/bash

# # brew_prefix=$(brew --prefix)

# # for pkg in $(brew list); do
# #     last_access=$(find "$brew_prefix/Cellar/$pkg" -type f -exec stat -f '%a' {} + | sort -n | tail -1)
# #     if [[ -n "$last_access" ]]; then
# #         echo "$pkg was last accessed on: $(date -r $last_access)"
# #     else
# #         echo "$pkg has no recorded access time"
# #     fi
# # done


