build-app:
	@docker compose up --build -d

ssh:
	@gcloud compute ssh 			\
		--project=${GCP_PROJECT_ID} \
		--zone=${GCP_ZONE_ID} 		\
		${GCP_VM_NAME}				

health-check:
	@$(eval RESP=`curl --write-out 	\
		"%{http_code}\n" 			\
		--silent 					\
		--output 					\
		/dev/null 					\
		http://${GCP_IP_ADDRESS}`)	\
		
	@bash deploy/check_app_health.sh ${RESP}
