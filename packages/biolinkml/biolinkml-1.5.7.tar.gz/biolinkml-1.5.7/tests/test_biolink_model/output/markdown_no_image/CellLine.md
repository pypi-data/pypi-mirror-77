
# Type: cell line




URI: [biolink:CellLine](https://w3id.org/biolink/vocab/CellLine)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[OrganismalEntity],[CellLineToThingAssociation],[CellLineToThingAssociation]-%20subject%201..1>[CellLine&#124;id(i):string;name(i):label_type;category(i):iri_type%20%2B],[OrganismalEntity]^-[CellLine])

## Parents

 *  is_a: [OrganismalEntity](OrganismalEntity.md) - A named entity that is either a part of an organism, a whole organism, population or clade of organisms, excluding molecular entities

## Referenced by class

 *  **[CellLineToThingAssociation](CellLineToThingAssociation.md)** *[cell line to thing association➞subject](cell_line_to_thing_association_subject.md)*  <sub>REQ</sub>  **[CellLine](CellLine.md)**

## Attributes


### Inherited from organismal entity:

 * [category](category.md)  <sub>1..*</sub>
    * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In a neo4j database this MAY correspond to the neo4j label tag
    * range: [IriType](types/IriType.md)
    * in subsets: (translator_minimal)
 * [id](id.md)  <sub>REQ</sub>
    * Description: A unique identifier for a thing. Must be either a CURIE shorthand for a URI or a complete URI
    * range: [String](types/String.md)
    * in subsets: (translator_minimal)
 * [name](name.md)  <sub>REQ</sub>
    * Description: A human-readable name for a thing
    * range: [LabelType](types/LabelType.md)
    * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | CLO:0000031 |

