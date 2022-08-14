<?php

if(!isset($argv) || !$argv[1])
{
	//$filename = "com02.out";
	die("\nCatSystem2 uncompressed binary to txt converter\nUsage: php convert.php filename.out\n");
}
else
	$filename = $argv[1];

if(!file_exists($filename))
{
	die("\nCatSystem2 uncompressed binary to txt converter\nFile does not exist: $filename\n");
}

$stem = explode(".", $filename);

//echo $filename;

$fp = fopen($filename, "rb");
$fo = fopen("..\\Text\\".$stem[0].".txt", "wt");

while(!feof($fp))
{
	$line = fgets($fp);

	$line = mb_convert_encoding($line, "UTF-8", "SJIS");
	
	$line = str_replace("\r", "", $line);
	
	$sp = explode("\t", $line);
	
	if(isset($sp[1]) && $sp[1] != "" && strlen($sp[1])>2)
	{
		$iscmd = false;
		
		//If there's a name tag, it's for sure a text line.
		if($sp[0] != "")
		{
			$iscmd = true;
		}

		//If the string starts with an english letter, it's a command and we ignore it.  Otherwise process away!
		$subst = substr($sp[1],0,2);
		if(preg_match("/^[a-zA-Z]/", $sp[1]) == 0 && ($subst != "\\n" || strlen($sp[1]) > 4))
			$iscmd = true;
		
		if($iscmd)
		{
			//I totally have this iscmd thing backwards. A command is supposed to be a line that doesn't have text!
			if($sp[0] == '')
				$sp[0] = "-";

			//$sp[1] = str_replace('\\n', '', $sp[1]);
			$sp[1] = str_replace('\\@', '', $sp[1]);
			//$sp[1] = str_replace('\\w0;', '', $sp[1]);

			$regex = "/\[(.+?)\/(.+?)\]/i";
			$replace = '$1';

			//Remove furigana
			//$sp[1] = preg_replace($regex, $replace, $sp[1]);

			$regex = "/([0-9+]) ([a-zA-Z0-9_]+) (.+)/i";
			$replace = '$3';

			//Extract the text from an option command.  Option lines will make it into
			//the $iscmd section because they start with numbers, not letters.
			$sp[1] = preg_replace($regex, $replace, $sp[1], -1, $cnt);
			if($cnt > 0)
				$sp[0] = "option";

			if($sp[1][0] != '#')
				//fwrite($fo, $sp[1]);
				fwrite($fo, $sp[0]."\t".$sp[1]);
		}
	}
}