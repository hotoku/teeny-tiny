a.out: out.c
	gcc $<


out.c:
	@python -m teeny hello.teeny


.PHONY: clean
clean:
	rm -f a.out out.c
