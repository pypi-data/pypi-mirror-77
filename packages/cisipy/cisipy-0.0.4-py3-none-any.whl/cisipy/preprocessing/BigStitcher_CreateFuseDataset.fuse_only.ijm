// read dataset path, number of tiles as commandline arguments
args = getArgument()
args = split(args, " ");
 
basePath = args[0];
if (!endsWith(basePath, File.separator))
{
    basePath = basePath + File.separator;
}
wellRound = args[1];
fusePath = args[2];
if (!endsWith(fusePath, File.separator))
{
    fusePath = fusePath + File.separator;
}

// fuse tiles
run("Fuse dataset ...",
	"select=" + basePath + wellRound + ".xml" +
	" process_angle=[All angles]" +
	" process_channel=[All channels]" +
	" process_illumination=[All illuminations]" +
	" process_tile=[All tiles]" +
	" process_timepoint=[All Timepoints]" +
	" bounding_box=[Currently Selected Views]" +
	" downsampling=1 pixel_type=[16-bit unsigned integer]" +
	" interpolation=[Linear Interpolation]" +
	" image=[Precompute Image]" +
	" interest_points_for_non_rigid=[-= Disable Non-Rigid =-]" +
	" blend preserve_original produce=[Each timepoint & channel]" +
	" fused_image=[Save as (compressed) TIFF stacks]" +
	" output_file_directory=" + fusePath +
	" filename_addition=" + wellRound);

// quit after we are finished
eval("script", "System.exit(0);");

