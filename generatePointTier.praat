#Automatically insert points to point tier from word tier word for annotated wav (each word repeated certain times)
#Point will be inserted at the mid point of each word and be labeled as the times of repetition
#27/02/2023 @LM

clearinfo

#information form
form Select audio file
	
	comment TG path should be long annotated/aligned/corrected TextGrid
	infile tg_path D:\data\lesson\emphatic lateral\TG\wav\EXP002_Onyx-Clean.TextGrid
	infile wav_path D:\data\lesson\emphatic lateral\TG\wav\EXP002_Onyx-Clean_ch1.wav
	positive word_tier 2
	positive point_tier 4
	positive repeatTime 3

endform

# Open wav file

tg = Read from file: tg_path$
tgDuration = Get total duration
wav = Read from file: wav_path$	
wavDuration = Get total duration
appendInfoLine: "wav: ", wav_path$

selectObject: tg
numInts = Get number of intervals: word_tier	

repetition = 1
nPoint = 0
for i to numInts
	start = Get start point... word_tier i
        	end   = Get end point... word_tier i
         	mid = (start+end)/2
         	select wav
         	select tg
         	if i < numInts
            		lab$ = Get label of interval... word_tier i
	    		appendInfoLine: lab$
	    		if lab$ <> ""
                		Insert point... point_tier mid
				nPoint += 1
				Set point text:  point_tier, nPoint, string$(repetition)
				repetition +=1
				if repetition > repeatTime
					repetition = 1
				endif
            		endif
         	endif
endfor

selectObject: tg
Save as text file: tg_path$ - ".TextGrid" + "_new.TextGrid"