# script to start services

echo "Starting application in ${APP_ENV} environment"

# if environment is development, enable the rabbitmq management tool 
if [ "$APP_ENV" == "development" ] 
then
   echo "Enabling management console for development environment"
   rabbitmq-plugins enable rabbitmq_management 
fi

echo "Starting rabbitmq server process "
service rabbitmq-server start

