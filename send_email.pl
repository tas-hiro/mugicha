#!/usr/bin/perl

use Net::SMTP;

$HOSTNAME=`/usr/bin/dig -x \$(/usr/bin/curl ifconfig.me) +short`;

$SMTP_SERVER = '127.0.0.1:25';
$FROM = "root\@$HOSTNAME";
$TO='recipient@example.com';

chomp($FROM,$TO,$HOSTNAME);

$HEADER="From: $FROM
To: $TO
Subject: S3 Upload is done.  $HOSTNAME
MIME-Version: 1.0
Content-type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 7bit

";

$BODY = "
本文

";


$smtp = Net::SMTP->new($SMTP_SERVER);
$smtp->mail($FROM);
$smtp->to($TO);
$smtp->data();
$smtp->datasend($HEADER);
$smtp->datasend($BODY);
$smtp->datasend();
$smtp->quit;
