# script to start services

echo "Starting application in ${APP_ENV} environment"

# if environment is development, enable the rabbitmq management tool 
if [ "$APP_ENV" == "development" ] 
then
   echo "Enabling management console for development environment"
   rabbitmq-plugins enable rabbitmq_management
   echo "Starting rabbitmq server process "
   service rabbitmq-server start
   echo "Adding admin user"
   rabbitmqctl add_user dev_inst dev_inst
   rabbitmqctl set_user_tags dev_inst administrator
   rabbitmqctl set_permissions -p / dev_inst ".*" ".*" ".*"
else
   echo "Starting rabbitmq server process "
   service rabbitmq-server start
fi


NUM_CORES=$( getconf _NPROCESSORS_ONLN )
echo "$NUM_CORES cpu cores detected on system"

echo "Starting nginx service"
service nginx start


source venv/bin/activate
if [ "$APP_ENV" == "development" ]
then 
   echo "Starting application in development mode"
   flask run -p 8000
else
   echo "Starting application with $NUM_CORES workers"
   gunicorn -w $NUM_CORES app:app
fi




