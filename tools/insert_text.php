<?php

if(!isset($argv) || !$argv[1])
{
	//$filename = "com02.out";
	die("\nCatSystem2 text -> script insertion tool\nUsage: php convert.php filename.out\n");
}
else
	$filename = $argv[1];

if(!file_exists($filename))
{
	die("\nCatSystem2 text -> script insertion tool\nFile does not exist: $filename\n");
}

$stem = explode(".", $filename);

//echo $filename;

$fp = fopen($filename, "rb");
$fp2 = fopen("..\\text\\$filename", "rb");

$output = "";

while(!feof($fp))
{
	$line = fgets($fp);
	
	$line = str_replace("\r", "", $line);
	$line = str_replace("\n", "", $line);
	
	$sp = explode("\t", $line);
	
	$needtrans = false;
	
	if(isset($sp[1]) && $sp[1] != "" && strlen($sp[1])>2)
	{
		$iscmd = false;
		
		if($sp[0] != "" && strlen($sp[1]) > 1)
		{
			$iscmd = true;
		}

		$subst = substr($sp[1],0,2);

		if(preg_match("/^[a-zA-Z]/", $sp[1]) == 0 && $subst[0] != '#' && ($subst != "\\n" || strlen($sp[1]) > 4))
			$iscmd = true;
		
		if($iscmd)
		{
			if($sp[0] == '')
				$sp[0] = "-";
			
			$trans = fgets($fp2);
			$trans = mb_convert_encoding($trans, "SJIS", "UTF-8");
			
			$trans = explode("\t", $trans);
			if(count($trans) > 1)
				$trans = $trans[1];
			else
				$trans = $trans[0];
			
			$trans = str_replace("\r", "", $trans);
			$trans = str_replace("\n", "", $trans);
			//$trans = str_replace("\t", "", $trans);
			
			$trans = str_replace("'", "`", $trans);	//Stupid system.  Backquotes are ugly.
			
			$regex = "/([0-9+]) ([a-zA-Z0-9_]+) (.+)/i";
			
			$cnt = preg_match($regex, $sp[1]);
			
			if($cnt > 0)
			{
				//Use fullwidth spaces for options.  Since engine won't accept normal ones.
				$trans = str_replace(" ", chr(0x81).chr(0x40), $trans);  
				$sp[1] = preg_replace($regex, "$1 $2 $trans", $sp[1]);
				
				$output .= "option\t$sp[1]\r\n";
			}
			else
			{
				//If it has a continue tag (\@), make sure to append it to the translated text.
				$cont = strpos($sp[1], "\\@");
				if($cont > 0)
					$trans .= "\\@";

				preg_match_all("/[\"0-9a-zA-Z]/i", $trans, $matches);
				$matches = $matches[0];
				if(count($matches) > strlen($trans)/2) //Hopefully will only catch english lines with this...
					$trans = wordwrap($trans, 56, "\\n", true);

				$output .= "$sp[0]\t$trans"."\r\n";
			}

		}
		else
			$output .= $line."\r\n";
	}
	else
		$output .= $line."\r\n";
}

fclose($fp);

file_put_contents($filename, $output);