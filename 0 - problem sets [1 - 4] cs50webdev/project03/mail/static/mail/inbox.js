document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

// Global variable to hide/show the "archive" button
let show_button = false;

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-header').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // By default, submit button is disabled
  const submitbutton = document.querySelector('#compose-submit');
  submitbutton.disabled = true;
  
  const fields = document.querySelectorAll('.form-control');
  
  // Function to check if submit button can be enabled
  function check_submit() {
    submitbutton.disabled = false;
    for (i = 0; i < (fields.length); i++) {
      if (fields[i].value.length < 1) {
        submitbutton.disabled = true;
        break;
      }
    }
  }

  // Checks if submit button can be enabled every time something is typed
  fields.forEach(function(fields) {
    fields.onkeyup = function() {
      check_submit();
    }
  });

  // On submit, make a POST REQUEST to /emails with the data
  document.querySelector('#compose-form').onsubmit = function() {
    const recipients = document.querySelector('#compose-recipients').value;
    const subject = document.querySelector('#compose-subject').value;
    const body = document.querySelector('#compose-body').value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
      })
    })
    .then(function(response) {
      return response.json();
    })
    .then(function(result) {
      alert(`${result.message}`);
      load_mailbox('sent');
    });
    return false;
  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-header').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#singular-email').style.display = 'none';
  document.querySelector('#all-emails').style.display = 'block';

  // Show the mailbox name
  const mailboxtitle = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`
  document.querySelector('#emails-header').innerHTML = mailboxtitle;

  // Clear "singular-email" div contents
  document.querySelector('#email-header').innerHTML = '';
  document.querySelector('#email-reply-button').innerHTML = '';
  document.querySelector('#email-body').innerHTML = '';

  // Handles the archive button variable based on what inbox is being loaded
  document.querySelector('#archive-button').style.display = 'none';
  show_button = false
  let sent_mailbox = true;
  if (mailbox === 'inbox' || mailbox === 'archive'){
    show_button = true;
    sent_mailbox = false;
  }

  // Fetches the emails
  fetch(`/emails/${mailbox}`)
  .then(function(response) {   // msm cois que: .then(response => response.json())
    return response.json();
  })
  .then(function(result) {   // msm coisa que: .then(emails => {
    
    // Displays the emails 
    const element = document.querySelector('#all-emails');
    load_emails(result, element, sent_mailbox);

    // Opens an email when it's clicked
    const email = document.querySelectorAll('.email-list');
    email.forEach(function(email) {
      email.addEventListener('click', function() {
        
        // Load clicked email
        load_email(email.id);
        
        // Mark email as read
        mark_as_read(email.id);
        
        // Show the selected email and hide mailbox
        document.querySelector('#singular-email').style.display = 'block';
        document.querySelector('#all-emails').style.display = 'none';
      })
    });
  });
}

// Loads all emails fetched
function load_emails(result, element, sent_mailbox) {
  const quantity = result.length;
  element.innerHTML = "";
  let background = "";
  for (i = 0; i < quantity; i++) {
    let email_adress = result[i].sender;
    if (sent_mailbox === true) {
      email_adress = `To: ${result[i].recipients}`
    }
    if (result[i].read === true) {
      background = 'rgb(228, 228, 228)';
    }
    else {
      background = 'white';
    };
    
    element.innerHTML = element.innerHTML + `
    <div id="${result[i].id}" class="email-list" style="background-color: ${background};">
      
      <div class="el-ss-container">
        <div class="el-sender">
        <span></span>
          ${email_adress}
        </div>
        <div class="el-subject">
          ${result[i].subject}
        </div>
      </div>

      <div class="el-t-container">
        <div class="el-time">
          ${result[i].timestampinbox}
        </div>
      </div>

    </div>
  `;
  }
}

// Loads content of clicked email 
function load_email(id) {
  fetch(`/emails/${id}`)
  .then(function(response) {
    return response.json();
  })
  .then(function(result) {

    // Renders the email
    const email_header = document.querySelector('#email-header');
    const email_body = document.querySelector('#email-body');
    const email_rb = document.querySelector('#email-reply-button');
    
    // Handles email header content
    email_header.innerHTML = `
        <b>From:</b> ${result.sender}<br>
        <b>To:</b> ${result.recipients}<br>
        <b>Subject:</b> ${result.subject}<br>
        <b>Timestamp:</b> ${result.timestamp}<br>
    `;
    // Handles email body content
    email_body.innerHTML = `<hr> ${result.body}`
    
    // Handles email reply button
    const reply_button = document.createElement('button');
    reply_button.id = 'reply-button'
    reply_button.className = "btn btn-sm btn-outline-primary"
    reply_button.innerHTML = 'Reply'
    reply_button.addEventListener('click', function() {
      reply(result);
    })
    email_rb.append(reply_button);

    // Handles archive button
    const buttondiv = document.querySelector('#archive-button');
    let button_name = ''
    // Handles archive button displayed name    
    if (result.archived === false) {
      button_name = 'Archive';
    }
    else {
      button_name = 'Unarchive';
    }
    // Shows/hides the archive button
    if (show_button === true){
      buttondiv.style.display = 'inline-block';
    }
    else {
      buttondiv.style.display = 'none';
    }
    // Creates the button and handles it's functionality
    const archive_button = document.createElement('button');
    archive_button.id = "archive-button"
    archive_button.className = "btn btn-sm btn-outline-primary"
    archive_button.innerHTML = `${button_name}`
    archive_button.addEventListener('click', function() {
      archive(id, archive_button, result.archived);
    })
    buttondiv.innerHTML = ""
    buttondiv.append(archive_button);
  });
}


// Archives/Unarchives emails
function archive(id, button, archived) {
  if (archived === false) {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
    .then(function() {
      load_mailbox('inbox');
    });
    button.innerHTML = 'Unarchive';
  }
  else {
    fetch(`/emails/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })
    .then(function() {
      load_mailbox('inbox');
    });
    button.innerHTML = 'Archive';
  }
}


// Marks email as read after being opened
function mark_as_read(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
}


function reply(email) {
  compose_email();
  document.querySelector('#compose-recipients').value = `${email.recipients}`;
  
  // Handles the "Re: " subject case
  document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  if (email.subject.slice(0, 4) === 'Re: ') {
    document.querySelector('#compose-subject').value = `${email.subject}`;
  }
  
  document.querySelector('#compose-body').value = `"On ${email.timestamp} ${email.sender} wrote:
  ${email.body}"`; 
}
