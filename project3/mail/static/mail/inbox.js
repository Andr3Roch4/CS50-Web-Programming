document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
 
}


function send_email() {
  // Send email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: `${document.querySelector('#compose-recipients').value}`,
      subject: `${document.querySelector('#compose-subject').value}`,
      body: `${document.querySelector('#compose-body').value}`
    })
  })
  .then(response => response.json())
  .catch(error => {
    console.log(error)
  })
  .then(result => {
    console.log(result);
    load_mailbox('inbox');
  })
}

 
function load_email(id) {
  // Hide compose view and emails view
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  if (document.querySelector('#email-info')) {
    document.querySelector('#email-info').remove();
  }
  if (document.querySelector('#body-div')) {
    document.querySelector('#body-div').remove();
  }
  // Load email content
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    const hdiv = document.createElement('div');
    hdiv.id = 'email-info';
    const from = document.createElement('h5');
    from.innerHTML = `<b>From: </b>${email.sender}`;
    hdiv.append(from);
    const to = document.createElement('h5');
    to.innerHTML = `<b>To: </b>${email.recipients}`;
    hdiv.append(to);
    const subject = document.createElement('h5');
    subject.innerHTML = `<b>Subject: </b>${email.subject}`;
    hdiv.append(subject);
    const timestamp = document.createElement('h5');
    timestamp.innerHTML = `<b>Timestamp: </b>${email.timestamp}`;
    hdiv.append(timestamp);
    const reply = document.createElement('button');
    reply.id = 'replybutton';
    reply.innerHTML = 'Reply';
    reply.classList.add('btn-primary');
    reply.addEventListener('click', () => {
      // Show compose view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#email-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      // Populate recipient field
      document.querySelector('#compose-recipients').value = `${email.sender}`;
      const str = 'RE:'
      if (email.subject.indexOf(str) >= 0) {
       document.querySelector('#compose-subject').value = `${email.subject}`;
      } else {
        document.querySelector('#compose-subject').value = `RE: ${email.subject}`;
      };
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
    });
    hdiv.append(reply);
    if (email.user !== email.sender) {  
      const archived = document.createElement('button');
      archived.id = 'archivebutton';
      archived.classList.add('btn-outline-secondary');
      if (email.archived === true) {
        archived.innerHTML = 'Unarchive';
        archived.addEventListener('click', () => {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: false
            })
          })
          .then(load_mailbox('inbox'));
        });
      } else {
        archived.innerHTML = 'Archive';
        archived.addEventListener('click', () => {
          fetch(`/emails/${email.id}`, {
            method: 'PUT',
            body: JSON.stringify({
              archived: true
            })
          })
          .then(load_mailbox('inbox'))
        })
      };
      hdiv.append(archived);
    }
    const bdiv = document.createElement('div');
    bdiv.id = 'body-div';
    bdiv.innerHTML = `<hr>${email.body}`;
    document.querySelector('#email-view').append(hdiv);
    document.querySelector('#email-view').append(bdiv);
  fetch(`/emails/${email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  })
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Load emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const emaildiv = document.createElement('div');
      emaildiv.style.border = 'solid';
      if (mailbox === 'sent') {
        const span1 = document.createElement('span');
        const span2 = document.createElement('span');
        span1.innerHTML = `<b>${email.recipients[0]}</b> ${email.subject}`;
        span2.innerHTML = `${email.timestamp}`;
        span2.style.position = 'absolute';
        span2.style.left = '75%';
        emaildiv.appendChild(span1);
        emaildiv.appendChild(span2);
      } else {
        const span1 = document.createElement('span');
        const span2 = document.createElement('span');
        span1.innerHTML = `<b>${email.sender}</b> ${email.subject}`;
        span2.innerHTML = `${email.timestamp}`;
        span2.style.position = 'absolute';
        span2.style.left = '75%';
        emaildiv.appendChild(span1);
        emaildiv.appendChild(span2);
      };
      emaildiv.id = 'email';
      if (email.read === true) {
        emaildiv.style.backgroundColor = 'lightgrey';
      } else {
        emaildiv.style.backgroundColor = 'white';
      };
      emaildiv.addEventListener('click', () => load_email(`${email.id}`));
      document.querySelector('#emails-view').append(emaildiv);
    }); 
  });
}