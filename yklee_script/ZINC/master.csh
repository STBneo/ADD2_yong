#!/bin/csh -f
foreach i (??)
	foreach j  ($i/????)
		pushd $j
		~/bin/scan.pl > log 
		popd
	end
end

