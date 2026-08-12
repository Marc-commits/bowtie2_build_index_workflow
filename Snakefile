configfile: "config/config.yaml"


include: "workflow/rules/build_index.smk"


rule bowtie2_build_index_workflow_all:
    """Convenience aggregate target for standalone runs/tests of this module.
    Consuming workflows should depend on this aggregator rule to maintain
    proper rule dependency hierarchy.
    """
    input:
        multiext(
            config["index_name"],
            ".1.bt2",
            ".2.bt2",
            ".3.bt2",
            ".4.bt2",
            ".rev.1.bt2",
            ".rev.2.bt2",
        ),
    default_target: True
