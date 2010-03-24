#!/usr/bin/perl -wT

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

#$CGI::POST_MAX = 1024 * 5000;
my $safe_filename_characters = "a-zA-Z0-9_.-/";


my $query = new CGI;
my $filename = $query->param("file_name");

my $return_dir = $query->param("path");

my $upload_dir = $query->param("directory");
$upload_dir =~ tr/ /_/;
$upload_dir =~ s/[^$safe_filename_characters]//g;

if ($upload_dir =~ /^([$safe_filename_characters]+)$/ ) 
{
  $upload_dir = $1;                     # $data now untainted
} else 
{
  die "Bad data in '$upload_dir'";      # log this somewhere
}




if ( !$filename )
{
 print $query->header ( );
 print "There was a problem uploading your file (try a smaller file).";
 exit;
}

my ( $name, $path, $extension ) = fileparse ( $filename, '/..*' );
$filename = $name . $extension;
$filename =~ tr/ /_/;
$filename =~ s/[^$safe_filename_characters]//g;

if ( $filename =~ /^([$safe_filename_characters]+)$/ )
{
 $filename = $1;
}
else
{
 die "Filename contains invalid characters";
}

$filename = $filename.".tmp";

my $upload_filehandle = $query->upload("file_name");

open ( UPLOADFILE, ">$upload_dir/$filename" ) or die "$!";
binmode UPLOADFILE;

while ( <$upload_filehandle> )
{
 print UPLOADFILE;
}

close UPLOADFILE;

print $query->header ( );

print <<END_HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
 <head>
    <title>Thanks!</title>
    <meta http-equiv="refresh" content="2;url=../cgi-bin/download_deformation_final.cgi">
 </head>
 <body>
   <p>Thanks for uploading a new deformation model!</p>
 </body>
</html>
END_HTML
