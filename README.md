# universal_user
# Build image
docker build  -t idehco3/universal_user:01 .
# Run image
docker run -e "IP_SGBD=your_ip_database"  -e "DATABASE_NAME=yourDatabase_name" -e "USER_NAME_DATABASE=your_user_name" -e "PASSWORD_DATABASE=your_password" -t -i idehco3/universal_user:01 /bin/bash

