#Function: Extratct sounds from annotated wav file; scale amplitude and add noise to the extracted sounds
#Purpose: For creating stimuli of AXB discrimination tasks
#This scripts requires certain praat scripts from praat VocalToolKit, please downloads VocalToolKit before using this script, and put required scripts to the same folder as this script(or put this script to the VocalToolKit scripts directory)
#28/02/2023 @LM from JH's Tutorial

clearinfo

#information form
form Select files
	
	comment TG should be corrected TextGrid and correspond to wav file
	
	infile tgPath Stimuli.TextGrid
	infile wavPath Stimuli.wav
	folder outDir Stimuli_normalized
	positive phraseTier 1
	positive wordTier 2
	positive segmentTier 3
	positive pointTier 4
	comment scale Peak
	positive scaledPeak 0.99
	comment add noise...
	positive noiseVolume 80
	optionmenu NoiseType: 2
		option White noise
		option Pink noise
		option Brown noise
	
endform

# Open files
tg = Read from file: tgPath$
tgDuration = Get total duration
wav = Read from file: wavPath$
wavDuration = Get total duration
appendInfoLine: "wav: ", wavPath$

selectObject: tg
nPoints = Get number of points: pointTier
for i from 1 to nPoints

	@processSound: i
	
endfor

procedure processSound: .num
	#get point 
	selectObject: tg
	pointLabel$ = Get label of point: pointTier, .num
	pointTime = Get time of point: pointTier, .num
	#get corresponding word interval
	wordInt = Get interval at time: wordTier, pointTime
	wordLabel$ = Get label of interval: wordTier, wordInt
	wordStart = Get start time of interval: wordTier, wordInt
	wordEnd = Get end time of interval: wordTier, wordInt
	appendInfoLine: wordLabel$
	#extract sound and tg
	tgPart = Extract part: wordStart, wordEnd, "yes"
	selectObject: wav
	soundPart = Extract part: wordStart, wordEnd, "rectangular", 1, "yes"
	#scale peak and add noise
	Scale peak: scaledPeak
	filename$ = outDir$ + "\" + wordLabel$ + "_" + pointLabel$ + "_" + string$(.num) + ".wav"
	runScript: "addnoise.praat", noiseVolume, noiseType$, "no"
	Save as WAV file: filename$
	
	#remove modified sound file here
	Remove 
	removeObject: tgPart
	removeObject: soundPart

endproc
