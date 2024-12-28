def algo_fmt(algo):
	name = algo
	lw = 2
	ls = "solid"
	color = None

	if algo == "reseek_fast":
		name = "Reseek (fast)"
		color = "black"
		ls = "dotted"
	elif algo == "reseek_sensitive":
		name = "Reseek (sensitive)"
		color = "black"
		ls = "dashed"
	elif algo == "reseek_verysensitive":
		name = "Reseek (verysensitive)"
		color = "black"

	elif algo == "reseek21_fast":
		name = "Reseek2.1 (fast)"
		color = "lightgray"
		ls = "dotted"
	elif algo == "reseek21_sensitive":
		name = "Reseek2.1 (sensitive)"
		color = "lightgray"
		ls = "dashed"
	elif algo == "reseek21_verysensitive":
		name = "Reseek2.1 (verysensitive)"
		color = "lightgray"

	elif algo == "blastp":
		name = "BLASTP"
		ls = "dotted"
		color = "lightgreen"
	elif algo == "dali":
		name = "DALI"
		color = "skyblue"
	elif algo == "tmalign" or algo == "TMalign":
		name = "TM-align"
		color = "magenta"
	elif algo == "foldseek":
		name = "Foldseek"
		lw = 3
		ls = "dotted"
		color = "orange"

	kwargs = {}
	kwargs["linewidth"] = lw
	kwargs["linestyle"] = ls
	if not color is None:
		kwargs["color"] = color
	return name, kwargs
