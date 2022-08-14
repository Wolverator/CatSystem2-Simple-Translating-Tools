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
$fo = fopen($stem[0].".txt", "wt");

$data = fread($fp,16);

$d = unpack("ILength/IOffset1/IOffset2/ICodeSection",$data);

function hexit($str)
{
	return "0x".str_pad(dechex($str), 8, "0", STR_PAD_LEFT);
	
}

//echo "Script Length: ".hexit($d['Length'])."\n";
//echo "Offset 1: ".hexit($d['Offset1'])."\n"; // wtf is offset 1 anyways
//echo "Offset 2: ".hexit($d['Offset2'])."\n";
//echo "Code Section: ".hexit($d['CodeSection'])."\n";

fwrite($fo, "#$stem[0]\n");

fseek($fp, $d['Offset2'] + 16);

$olen = ($d['CodeSection'] - $d['Offset2'])/4;

$header = $d;

//echo "Number of script entries: " . $olen."\n";

$arr = array();

for($i = 0; $i < $olen; $i++)
{
	$data = fread($fp,4);
	$d = unpack("I", $data);

	$arr[$i] = $d[1];

	//echo hexit($arr[$i])."\n";
}

function realpos($offset)
{
	global $header;
	return $offset + $header['CodeSection'] + 16;	
}

function readstring()
{
	global $fp;
	global $fo;
	
	$data = fread($fp,1);
	$d = unpack("c", $data);
	$cmd = $d[1];
	
	$data = fread($fp,1);
	$d = unpack("c", $data);
	$cmd .= $d[1];
	
	//echo "(CMD$cmd) ";
	
	$txt = "";
	while($txt != '\0')
	{
		$data = fread($fp,1);
		$d = unpack("C", $data);
		
		//echo $d[1];
		if($d[1] == 0)
			break;
		
		if(feof($fp))
			break;
		
		$txt .= $data;
	}
	if($cmd == 133)
		fwrite($fo, "$txt");
	elseif($cmd == 132 && $txt == '')
		fwrite($fo, "\t\\n\n");
	else
		fwrite($fo, "\t$txt\n");
}

for($i = 0; $i < count($arr); $i++)
{
	fseek($fp, realpos($arr[$i]));
	//echo hexit(realpos($arr[$i])).": ";
	readstring();
	
//	if($i > 100)
//		die();
}

echo "Converted binary and created output file ".$stem[0].".txt.";