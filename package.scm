(use-modules (guix packages)
	(guix gexp)
	((guix licenses) #:prefix license:)
	(guix build-system python))

(package
	(name "DanielPreconfig")
	(version "2.1")
	(inputs '())
	(native-inputs '())
	(propagated-inputs '())
	(source (local-file "./src" #:recursive? #t))
	(build-system python-build-system)
	(synopsis "daniel_preconfig: config pre-processor")
	(description
		"Daniel_Preconfig generates files from a template by evaluating double-bracketed Python code.")
	(home-page "https://github.com/danielbatterystapler/preconfig")
	(license license:gpl3))

