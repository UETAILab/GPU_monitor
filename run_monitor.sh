export MACHINE_ID=test_id
export GPU_MEMORY_THRESHOLD=100
export CALLBACK_URL=http://localhost:5000/sysreport
export SENDER_EMAIL_ADDRESS=uetailab.alert@gmail.com
export SENDER_EMAIL_PASSWORD=uetailab@123
export RECIEVER_EMAIL_LIST="caohoangtung2001@gmail.com caohoangtung201@gmail.com 19020055@vnu.edu.vn"

current_dir="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
python3 $current_dir/tracker.py --machine_id $MACHINE_ID --gpu_memory_threshold $GPU_MEMORY_THRESHOLD --callback_url $CALLBACK_URL --sender_email_address $SENDER_EMAIL_ADDRESS --sender_email_password $SENDER_EMAIL_PASSWORD --receiver_email_list $RECIEVER_EMAIL_LIST
