from typing import Literal


def extend_flexion(title, text, current_record):
    """
    1. Alle flexion keys sind lowercase
    2. Ergänze adjektivische Deklinationen, die von der Vorlage autom. ausgefüllt werden und nicht im Wikitext stehen

    Vorlage: https://de.wiktionary.org/wiki/Vorlage:Deutsch_adjektivisch_%C3%9Cbersicht
    """

    if "flexion" not in current_record:
        return False

    # make keys lowercase
    flexion_dict = {k.lower(): v for k, v in current_record["flexion"].items()}

    if "{{Deutsch adjektivisch Übersicht" not in text:
        return {"flexion": flexion_dict}

    if "genus" not in flexion_dict or flexion_dict["genus"] not in ["f", "m", "n"]:
        return {"flexion": flexion_dict}

    if "stamm" not in flexion_dict:
        return {"flexion": flexion_dict}

    kein_singular = "kein singular" in flexion_dict and flexion_dict[
        "kein singular"
    ].lower() in ["1", "ja"]
    kein_plural = "kein plural" in flexion_dict and flexion_dict[
        "kein plural"
    ].lower() in ["1", "ja"]

    stamm = flexion_dict["stamm"]
    genus: Literal["f", "m", "n"] = flexion_dict["genus"]

    if "nominativ singular stark" not in flexion_dict and kein_singular is False:
        if genus == "m":
            form = stamm + "r"
        elif genus == "f":
            form = stamm
        elif genus == "n":
            form = stamm + "s"

        flexion_dict["nominativ singular stark"] = form

    if "nominativ plural stark" not in flexion_dict and kein_plural is False:
        flexion_dict["nominativ plural stark"] = stamm

    if "genitiv singular stark" not in flexion_dict and kein_singular is False:
        if genus == "m":
            form = stamm + "n"
        elif genus == "f":
            form = stamm + "r"
        elif genus == "n":
            form = stamm + "n"

        flexion_dict["genitiv singular stark"] = form

    if "genitiv plural stark" not in flexion_dict and kein_plural is False:
        flexion_dict["genitiv plural stark"] = stamm + "r"

    if "dativ singular stark" not in flexion_dict and kein_singular is False:
        if genus == "m":
            form = stamm + "m"
        elif genus == "f":
            form = stamm + "r"
        elif genus == "n":
            form = stamm + "m"

        flexion_dict["dativ singular stark"] = form

    if "dativ plural stark" not in flexion_dict and kein_plural is False:
        flexion_dict["dativ plural stark"] = stamm + "n"

    if "akkusativ singular stark" not in flexion_dict and kein_singular is False:
        if genus == "m":
            form = stamm + "n"
        elif genus == "f":
            form = stamm
        elif genus == "n":
            form = stamm + "s"

        flexion_dict["akkusativ singular stark"] = form

    if "akkusativ plural stark" not in flexion_dict and kein_plural is False:
        flexion_dict["akkusativ plural stark"] = stamm

    if "nominativ singular schwach" not in flexion_dict and kein_singular is False:
        flexion_dict["nominativ singular schwach"] = stamm

    if "nominativ plural schwach" not in flexion_dict and kein_plural is False:
        flexion_dict["nominativ plural schwach"] = stamm + "n"

    if "genitiv singular schwach" not in flexion_dict and kein_singular is False:
        flexion_dict["genitiv singular schwach"] = stamm + "n"

    if "genitiv plural schwach" not in flexion_dict and kein_plural is False:
        flexion_dict["genitiv plural schwach"] = stamm + "n"

    if "dativ singular schwach" not in flexion_dict and kein_singular is False:
        flexion_dict["dativ singular schwach"] = stamm + "n"

    if "dativ plural schwach" not in flexion_dict and kein_plural is False:
        flexion_dict["dativ plural schwach"] = stamm + "n"

    if "akkusativ singular schwach" not in flexion_dict and kein_singular is False:
        if genus == "m":
            form = stamm + "n"
        else:
            form = stamm

        flexion_dict["akkusativ singular schwach"] = form

    if "akkusativ plural schwach" not in flexion_dict and kein_plural is False:
        flexion_dict["akkusativ plural schwach"] = stamm + "n"

    if "nominativ singular gemischt" not in flexion_dict and kein_singular is False:
        if genus == "m":
            form = stamm + "r"
        elif genus == "f":
            form = stamm
        elif genus == "n":
            form = stamm + "s"

        flexion_dict["nominativ singular gemischt"] = form

    if "nominativ plural gemischt" not in flexion_dict and kein_plural is False:
        flexion_dict["nominativ plural gemischt"] = stamm

    if "genitiv singular gemischt" not in flexion_dict and kein_singular is False:
        flexion_dict["genitiv singular gemischt"] = stamm + "n"

    if "genitiv plural gemischt" not in flexion_dict and kein_plural is False:
        flexion_dict["genitiv plural gemischt"] = stamm + "n"

    if "dativ singular gemischt" not in flexion_dict and kein_singular is False:
        flexion_dict["dativ singular gemischt"] = stamm + "n"

    if "dativ plural gemischt" not in flexion_dict and kein_plural is False:
        flexion_dict["dativ plural gemischt"] = stamm + "n"

    if "akkusativ singular gemischt" not in flexion_dict and kein_singular is False:
        if genus == "m":
            form = stamm + "n"
        elif genus == "f":
            form = stamm
        elif genus == "n":
            form = stamm + "s"

        flexion_dict["akkusativ singular gemischt"] = form

    if "akkusativ plural gemischt" not in flexion_dict and kein_plural is False:
        flexion_dict["akkusativ plural gemischt"] = stamm

    return {"flexion": flexion_dict}
