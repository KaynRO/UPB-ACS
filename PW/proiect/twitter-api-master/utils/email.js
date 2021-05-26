const nodeMailer = require('nodemailer');
const ejs = require('ejs');
const htmlToText = require('html-to-text');

const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const sendMail = async (options) => {
   // https://github.com/sendgrid/sendgrid-nodejs

   const html = await ejs.renderFile(
      `${__dirname}/../views/email/${options.template}`,
      {
         user: options.user,
         url: options.url,
      }
   );

   const msg = {
      from: process.env.Email_From,
      to: options.email,
      subject: options.subject,
      html,
   };

   sgMail
      .send(msg)
      .then(() => {
         console.log('Email sent');
      })
      .catch((error) => {
         console.error(error);
      });

};
module.exports = sendMail;
