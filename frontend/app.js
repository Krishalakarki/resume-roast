// const API = "https://resume-roast-2.onrender.com";
const API = "http://127.0.0.1:8000";


// =======================
// SIGNUP
// =======================
async function signup() {

    const email = document.getElementById("signupEmail").value;
    const password = document.getElementById("signupPassword").value;

    const response = await fetch(`${API}/auth/signup`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    alert(data.message);
    window.location.href = "login.html";
}


// =======================
// LOGIN
// =======================
async function login() {

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    const response = await fetch(`${API}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (data.access_token) {

        localStorage.setItem(
            "token",
            data.access_token
        );

        window.location.href = "dashboard.html";

    } else {

        alert("Login failed");

    }
}



// =======================
// UPLOAD RESUME
// =======================
async function uploadResume() {

    const file =
    document.getElementById("resumeFile").files[0];

    const token =
    localStorage.getItem("token");


    const formData = new FormData();

    formData.append(
        "file",
        file
    );


    const response = await fetch(
        `${API}/llm_analyze/analyze`,
        {
            method:"POST",

            headers:{
                "Authorization":
                `Bearer ${token}`
            },

            body:formData
        }
    );


    const data =
    await response.json();


    const aiText =
    data.result || "No response found";


    document.getElementById("result").innerText =
    aiText;

}





// =======================
// LOAD HISTORY
// =======================
async function loadHistory() {


    const token =
    localStorage.getItem("token");


    const res = await fetch(
        `${API}/llm_analyze/history`,
        {

        method:"GET",

        headers:{
            "Authorization":
            `Bearer ${token}`
        }

        }
    );


    const data =
    await res.json();



    const container =
    document.getElementById("historyList");


    container.innerHTML = "";



    data.forEach(item => {


        const div =
        document.createElement("div");


        div.className =
        "history-item";


        div.innerText =
        item.filename;



        div.onclick = () => {


            const text =
            item.ai_response || "No data";


            document.getElementById("result")
            .innerText = text;


        };


        container.appendChild(div);


    });

}



// =======================
// PAYMENT STATUS
// =======================
async function checkPayment(){


    const token =
    localStorage.getItem("token");


    const res = await fetch(
        `${API}/payment/status`,
        {

        headers:{
            "Authorization":
            `Bearer ${token}`
        }

        }
    );


    const data =
    await res.json();



    const box =
    document.getElementById("paymentBox");



    if(!box) return;



    if(data.paid){


        box.innerHTML =
        `
        <h3>
        ✅ Premium unlocked
        </h3>
        `;


    }

    else{


        box.innerHTML =
        `
        <button 
        class="primary-btn"
        onclick="payNow()">

        Unlock Premium Roast - Rs 199

        </button>
        `;

    }

}





// =======================
// ESEWA PAYMENT
// =======================
async function payNow(){


    const token =
    localStorage.getItem("token");



    const res = await fetch(
        `${API}/payment/create`,
        {

        method:"POST",

        headers:{
            "Authorization":
            `Bearer ${token}`
        }

        }
    );



    const data =
    await res.json();



    const form =
    document.createElement("form");


    form.method = "POST";

    form.action =
    data.payment_url;



    const fields = {


        amount:data.amount,


        tax_amount:0,


        total_amount:data.amount,


        transaction_uuid:
        data.transaction_uuid,


        product_code:
        data.product_code,


        product_service_charge:0,


        product_delivery_charge:0,


        success_url:
        
        "http://127.0.0.1:8000/payment/success",


        failure_url:
        
         "http://localhost:5500/dashboard.html",



        signed_field_names:
        "total_amount,transaction_uuid,product_code",


        signature:
        data.signature
        

    };



    for(const key in fields){


        const input =
        document.createElement("input");


        input.type="hidden";


        input.name=key;


        input.value=fields[key];


        form.appendChild(input);

    }



    document.body.appendChild(form);


    form.submit();


}




// =======================
// ON PAGE LOAD
// =======================
window.onload = () => {


    if(localStorage.getItem("token")){


        loadHistory();


        checkPayment();


    }

};