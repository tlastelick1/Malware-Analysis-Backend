import sys
import src.osa as osa
import src.names as names
import src.maths as maths
import src.object_handler as object_handler
import src.string_escaper as string_escaper
import src.basic_expressions as basic_expressions


def build_output_path(input_path: str):
    return __import__("os").path.join("/".join(input_path.split("/")[0:-1]), "output.js")


def usage():
    print("The input JS file is missing.\n\nUsage :\npython3 %s <source.js>" % (__file__))


def deobfuscate(source: str) -> str:
    osa_name = osa.find_osa_name(source)
    if osa_name is not None:
        osa_content = osa.get_osa_content(source)
        source = osa.use_osa_content(source, osa_name, osa_content)

    source = names.unused_names(source)
    source = names.replace_names(source)
    source = basic_expressions.booleans(source)
    source = basic_expressions.integers(source)
    source = basic_expressions.operators(source)
    source = string_escaper.escape_string(source)
    source = object_handler.dict_to_obj(source)
    source = maths.do_the_maths(source)
    source = names.remove_unused_function(source)
    source = source.replace("\n", "")
    return source


def main():
    if len(sys.argv) < 2:
        return usage()

    input_path = sys.argv[1]
    with open(input_path, "r", encoding="utf-8") as stream:
        source = stream.read()

    source = deobfuscate(source).encode("utf-8", "ignore")

    output_path = build_output_path(input_path)
    with open(output_path, 'wb+') as stream:
        stream.write(source)


if __name__ == "__main__":
    main()
