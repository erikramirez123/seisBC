from turtle import done


$ sac2mseed CI*

# Then, remove the *.mseed of the files:
# 
# ###################################
for i in CI.*; do
    mv "$i" "${f%.mseed}"
done
