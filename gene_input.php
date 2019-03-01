<html>
<?php

set_time_limit(2000);

echo '<html>
<head>
<title>CAT Tools</title>
<link rel="icon" href="https://img.icons8.com/color/64/000000/cat.png">
<!-- Font Awesome -->
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css">
<!-- Bootstrap core CSS -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.2.1/css/bootstrap.min.css" rel="stylesheet">
<!-- Material Design Bootstrap -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.7.3/css/mdb.min.css" rel="stylesheet">
<!-- JQuery -->
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<!-- Bootstrap tooltips -->
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.4/umd/popper.min.js"></script>
<!-- Bootstrap core JavaScript -->
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.2.1/js/bootstrap.min.js"></script>
<!-- MDB core JavaScript -->
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.7.3/js/mdb.min.js"></script>

</head>

<body>';

echo '
<center><div><img style="margin-top: -60px" src="https://img.icons8.com/color/100/000000/cat.png"><h1 class="display-1 orange-text" style="display: inline;">CAT Tools</h1></div>
<h3 class="grey-text" style="">Chloé, Alba, Thomas Tools</h3>

<a class="btn blue-gradient" href="../">Return to selection page</a><br>';

if ($_SERVER['REQUEST_METHOD'] == 'POST') 
{
	$dest = '';
	if (is_uploaded_file($_FILES['import_file']['tmp_name'])) 
	  { 
		//First, Validate the file name
		if(empty($_FILES['import_file']['name']))
		{
			echo " File name is empty! ";
			exit;
		}
	 
		$upload_file_name = $_FILES['import_file']['name'];
		//Too long file name?
		if(strlen ($upload_file_name)> 100)
		{
			echo " too long file name ";
			exit;
		}
	 
		//replace any non-alpha-numeric caracters in th file name
		$upload_file_name = preg_replace("/[^A-Za-z0-9 \.\-_]/", '', $upload_file_name);
	 
		//set a limit to the file upload size
		if ($_FILES['import_file']['size'] > 1000000) 
		{
			echo " too big file ";
			exit;        
		}
	 
		//Save the file
		$dest=__DIR__.'/'.$upload_file_name;
		
		if (move_uploaded_file($_FILES['import_file']['tmp_name'], $dest)) 
		{
			echo $upload_file_name . ' File Has Been Uploaded !<br>';

		}
	  }
	$path = $_POST["script_name"];
	$fullpath = $path . "_script/main.py";

	$result = exec("python3 " . $fullpath . " 2>&1 " . $dest, $output ,$return);

	if ($return == 1){
		echo "<p class=\"text-warning\">Error Go Back to the Selection Page</p></center>";
		echo $result;
		echo $return;
	}else{
		$result_path = $path . '_script/result.html';
	echo '<a class="btn blue-gradient" href="' . $result_path . '" target="_blank">Opens On Another Tab</a></center>';
	}

}

?>
</html>
