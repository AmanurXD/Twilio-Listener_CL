from flask import Flask, request, jsonify
import requests  # <-- NEW IMPORT
import random    # <-- NEW IMPORT
import urllib.parse # <-- NEW IMPORT

app = Flask(__name__)

# A simple in-memory dictionary to store messages.
MESSAGES_RECEIVED = {}

# ====================================================================
# ======= SECTION 1: NEW HELPER DATA FOR THE FORM SUBMITTER ========
# ====================================================================
# --- Data for Random Generation ---
USA_FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
USA_LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
PROGRAM_OPTIONS = ['29', '344'] # '29' = After School, '344' = Summer Camp
# The domain for generating random emails
FORM_SUBMISSION_DOMAIN = "codewithjames.top"
# ====================================================================


@app.route('/sms', methods=['POST'])
def receive_sms():
    """Endpoint for Twilio to send SMS data to."""
    try:
        to_number = request.form.get('To')
        message_body = request.form.get('Body')
        
        if not to_number or not message_body:
            return "Missing data", 400
        
        MESSAGES_RECEIVED[to_number] = message_body
        
        print(f"Received message for {to_number}: '{message_body}'")
        return "<Response></Response>", 200
    except Exception as e:
        print(f"Error in /sms: {e}")
        return "Server Error", 500

@app.route('/get-message/<phone_number>', methods=['GET'])
def get_message(phone_number):
    """Endpoint for the local client to poll for a message."""
    if phone_number in MESSAGES_RECEIVED:
        message = MESSAGES_RECEIVED[phone_number]
        del MESSAGES_RECEIVED[phone_number]
        return jsonify({"status": "found", "body": message})
    else:
        return jsonify({"status": "not_found"})

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint for Render."""
    return "OK", 200

# ====================================================================
# ======= SECTION 2: NEW BROWSER-LESS FORM SUBMISSION ENDPOINT =======
# ====================================================================
@app.route("/submit-cranford-form", methods=["GET"])
def submit_cranford_form():
    phone_number = request.args.get('number')
    if not phone_number:
        return jsonify({"error": "Missing required 'number' parameter."}), 400

    # 1. Generate Random Data
    first_name = random.choice(USA_FIRST_NAMES)
    last_name = random.choice(USA_LAST_NAMES)
    random_name = f"{first_name} {last_name}"
    random_email_alias = f"{first_name.lower()}.{last_name.lower()}{random.randint(10,999)}"
    random_email = f"{random_email_alias}@{FORM_SUBMISSION_DOMAIN}"
    random_program = random.choice(PROGRAM_OPTIONS)
    
    print(f"[Cranford Form] Generated data: Name='{random_name}', Email='{random_email}', Phone='{phone_number}', Program='{random_program}'")

    # 2. Prepare the payload with our reusable "Master Key" token
    reusable_grctoken = "0cAFcWeA7hsprh2jNZRG_mE7AgbuZZ7DhWIuVRGTyRgBrl0BgcCvkHhMVUX8otBUaHly7sTg08nwJXVpb8HdWXVp3qvyfE-RmZNKQb0J4MITs96oXVLcblDEnaHFuTmbjqh6iTC7BZ3yUgIwwCkQqK5AR-Ytmt_7FEaMsYow-OSlvZus8LA1aujPQHm1mRkHmtF7elEIKmK3SNwALBSXLV874ywT4DoKZGYj-K8egjXtjMRj6032EndcPgA1sxpwUOqBbeUla-uYh-EQTQ9ChBAGDcFUsaMyGbx57feZVXTka0Do4QtAW2xtPoGTCG5ugZT76Wn_LfDo33jvzakKPV_tLB94x2Ku99-NrviFKAJSkLHsN_2Sj4pbhs0_Z8CQPX42dUfZR7AdM6qI8UiEHFnGN9yl6GzmYUGWXwF-yM_0_dHjGjZgNsFK2E95i1Zi6_vKExpgFyUJu0eGR2nQ5Zdh-20Pwpwz2XB62Jw_jsGhvfFzDPHN98uvcQb0u5rIZ5BzoQ8w468gpOtAEDVt4bV5u5Kx5TbwJs0VdlNz8BFWAqG3W7ewOdsDnSeFzYs_0YdUOiKs-nRwLeaNTFrSzxks4X1TIFTMIlVHUt5gxMS1N5seuQNIfZYnPJNbUCj_upguTqaISBOUMmju5N3kHcBFPRfffh_6n1dfhhKhu6rGCheXB6p7e8OjKhMp8Dk9_wwKdsExXjys1l9nR3hoMYgAN_4XPQPF-cLD4njVLy1qbL-tIk5hZsULeAOkTMIDiFjmM6StGDWPYPmZN1e-SR7SC13m9Jc5DDOePjU7YvzO3L6gpgjFFxF7LpS20e7azzXqsoQ3dlBkOEgRnIXEYIkM84kgPgP0GkHXwHHXisDMPjJmBTaQb0PX_2L_u6Jj2nqJO4ii9pmHGbGowcnI9F2QW8BEkH3Cc4xw11mwEkrhl_yHNPLEoOtc7KMRW_I9vEjLEYfYMkQp2k6b_7j-FMQNZgz0SkZGo3mW6ZgUJ3qErD2C1BbwJ0RprTMgRqe_dpjoik6H2-iM_fXC5Ka-iQtBpXaAtBzlyCZuSyv_1gYJlN68Q8eez__j795Q1lV0f-N0g1G-fRzBEKd6BCoRZJE7l_f951s2mybqH1jDAx1wULYt1ckY3gKVFgciKhQKzEII_oKLVe4VzxtwlTkyEmjsVJjDiynYFB3VKc1XMym2IFd3e71wwK7p5sXgnYu_x2a04uB9TxtZm46NCQizxlAjiwCDSB2CVSkaYNbpXM2OC9FnRc2bEPELlYR6a9_dnuTGs4bccqGJYhFUkndsFqoOoZZ1VushzavzQg4Vddqce4s9khuQelCXcwhL-w4QEeLY2DZfSsjyTpwZxe5MrCo4bhpt9EaqbxUGJKNfj6mTaJA8SConco5VdRWS553ChKV3nbzhUzGRfXvRFT4qd9XhJ1CzcsRmNLTCQMi5n1H3BoFkE0HbPawxosFnpTMvyeacAZrS77mw3q_2n2dZvBFPgvDzVxqz-Yla-TILwCF-4T9X-H8oecqrAAdiK_TGz8Kd7Bz40pjv_XAOg5aceOLoPJ-brdpkzTC9bDsPPLTclSHM1P9y3iGxcPkTojp0f2GsZV1Zt0uRnNjl64ADdUCnKUmmgzo58gGuKU9PbiTuRn9cmv5BUVDwxI"
    
    payload_dict = {
        "full_name": random_name,
        "email": random_email,
        "phone": phone_number,
        "program_id": random_program,
        "location": "cranford-nj",
        "contact_method": "",
        "action": "mm_custom_form_home_submit",
        "mmcrm_original_landing_page": "https://cranfordsbestkids.com/",
        "grctoken": reusable_grctoken
    }
    payload_string = urllib.parse.urlencode(payload_dict)

    # 3. Perform the fast, direct submission
    submission_url = "https://cranfordsbestkids.com/wp-admin/admin-ajax.php"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'origin': 'https://cranfordsbestkids.com',
        'referer': 'https://cranfordsbestkids.com/',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    try:
        print("[Cranford Form] Sending fast, direct request...")
        response = requests.post(submission_url, headers=headers, data=payload_string, timeout=10)
        response.raise_for_status()
        
        response_json = response.json()

        if response_json.get("status") == 1:
            print("[Cranford Form] SUCCESS: Server confirmed submission.")
            return jsonify({
                "status": "success",
                "message": "Form submitted successfully.",
                "submitted_data": { "name": random_name, "email": random_email, "phone": phone_number }
            }), 200
        else:
            print(f"[Cranford Form] FAILURE: Server responded with non-success status: {response.text}")
            return jsonify({"status": "failure", "server_response": response_json}), 502

    except requests.exceptions.RequestException as e:
        print(f"[Cranford Form] ERROR: Network request to submission URL failed: {e}")
        return jsonify({"error": f"Failed to send final request: {e}"}), 500
# ====================================================================


if __name__ == '__main__':
    app.run(port=5000)
