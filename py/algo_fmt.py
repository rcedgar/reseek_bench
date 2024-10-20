def algo_fmt(algo):
	name = algo
	lw = 2
	ls = "solid"
	color = None

	if algo == "reseek_fast":
		name = "Reseek (fast)"
		color = "black"
		lw = 3
		ls = "dotted"
	elif algo == "reseek_v1.2":
		name = "Reseek v1.2"
		color = "gray"
	elif algo == "reseek_verysensitive":
		name = "Reseek (verysensitive)"
		color = "gray"
		ls = "dashed"
	elif algo == "reseek_sensitive":
		name = "Reseek (sensitive)"
		color = "black"
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
