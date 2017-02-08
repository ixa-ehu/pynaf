
from __future__ import unicode_literals

"""Module for manage NAF formatted files. """

from logging import getLogger
from lxml import etree
#from xml import etree
__author__ = 'Rodrigo Agerri <rodrigo.agerri@ehu.es>'


class NAFDocument:
    """ Manage a NAF document.
    """
    # CONSTANT TEXT VALUES USED TO CONSTRUCT NAF
    KAF_TAG = "NAF"
    LANGUAGE_ATTRIBUTE = "{http://www.w3.org/XML/1998/namespace}lang"
    VERSION_ATTRIBUTE = "version"
    NS = {}

    KAF_HEADER_TAG = "nafHeader"
    NAME_ATTRIBUTE = "name"
    LINGUISTIC_PROCESSOR_HEAD = "linguisticProcessors"
    LAYER_ATTRIBUTE = "layer"
    LINGUISTIC_PROCESSOR_OCCURRENCE_TAG = "lp"
    BEGIN_TIMESTAMP_ATTRIBUTE = "beginTimestamp"
    END_TIMESTAMP_ATTRIBUTE = "endTimestamp"
    HOSTNAME_ATTRIBUTE = "hostname"
    # Text layer
    TEXT_LAYER_TAG = "text"
    WORD_OCCURRENCE_TAG = "wf"
    WORD_ID_ATTRIBUTE = "id"

    # Term layer
    TERMS_LAYER_TAG = "terms"
    TERM_OCCURRENCE_TAG = "term"
    TERM_ID_ATTRIBUTE = "id"
    NER_ATTRIBUTE = "ner"
    TYPE_ATTRIBUTE = "type"
    LEMMA_ATTRIBUTE = "lemma"
    POS_ATTRIBUTE = "pos"
    MORPHOFEAT_ATTRIBUTE = "morphofeat"

    # Chunking layer
    CHUNKS_LAYER_TAG = "chunks"
    CHUNK_OCCURRENCE_TAG = "chunk"
    CHUNK_CASE_ATTRIBUTE = "case"
    CHUNK_PHRASE_ATTRIBUTE = "phrase"
    CHUNK_HEAD_ATTRIBUTE = "head"
    CHUNK_ID_ATTRIBUTE = "cid"

    # Constituency Layer
    CONSTITUENCY_LAYER = "constituency"
    CONSTITUENCY_TREE_TAG = "tree"
    CONSTITUENCY_ID_ATTRIBUTE = "id"
    CONSTITUENCY_LABEL_ATTRIBUTE = "label"
    CONSTITUENCY_NON_TERMINALS = "nt"
    CONSTITUENCY_TERMINALS = "t"
    CONSTITUENCY_EDGES = "edge"
    CONSTITUENCY_EDGE_ID_ATTRIBUTE = "id"
    CONSTITUENCY_EDGE_FORM_ATTRIBUTE = "from"
    CONSTITUENCY_EDGE_TO_ATTRIBUTE = "to"

    # Dependency Layer
    DEPENDENCY_LAYER_TAG = "deps"
    DEPENDENCY_OCCURRENCE_TAG = "dep"
    DEPENDENCY_FROM_ATTRIBUTE = "from"
    DEPENDENCY_FUNCTION_ATTRIBUTE = "rfunc"
    DEPENDENCY_TO_ATTRIBUTE = "to"

    # Coreference Layer
    COREFERENCE_LAYER_TAG = "coreferences"
    COREFERENCE_ID_ATTRIBUTE = "id"
    COREFERENCE_OCCURRENCE_TAG = "coref"

    # Name Entity layer
    NAMED_ENTITIES_LAYER_TAG = "entities"
    NAMED_ENTITY_OCCURRENCE_TAG = "entity"
    NAMED_ENTITY_ID_ATTRIBUTE = "id"
    NAMED_ENTITY_TYPE_ATTRIBUTE = "type"
    NAMED_ENTITY_REFERENCES_GROUP_TAG = "references"

    # References tags
    SPAN_TAG = "span"
    TARGET_ID_ATTRIBUTE = "id"
    TARGET_TAG = "target"

    # External references

    EXTERNAL_REFERENCE_OCCURRENCE_TAG = "externalRef"
    EXTERNAL_REFERENCES_TAG = "externalReferences"

    valid_word_attributes = ("sent", "para", "offset", "length", "page")
    valid_external_attributes = ("resource", "reference", "reftype", "status",
                                 "source", "confidence")
    valid_externalRef_attributes = ("resource", "reference")

    def __init__(self, file_name=None, input_stream=None, language=None,
                 version="2.0", header=None, encoding="utf-8",
                 dtd_validation=False):
        """ Prepare the document basic structure."""
        self.encoding = encoding
        self.logger = getLogger(__name__)
        parser = etree.XMLParser(
            remove_comments=False, dtd_validation=dtd_validation)
        etree.set_default_parser(parser)

        if file_name:
            self.tree = etree.parse(file_name)
            self.root = self.tree.getroot()
        elif input_stream:
            if isinstance(input_stream, unicode):
                input_stream = input_stream.encode(encoding)
            self.root = etree.fromstring(input_stream)
            self.tree = etree.ElementTree(self.root)
        else:
            self.root = etree.Element(self.KAF_TAG, self.NS)
            self.tree = etree.ElementTree(self.root)
        if language:
            self.root.attrib[self.LANGUAGE_ATTRIBUTE] = language

        if version:
            self.root.set(self.VERSION_ATTRIBUTE, version)

        headers = self.tree.find(self.KAF_HEADER_TAG)
        if headers is not None and len(headers):
            self.kaf_header = headers
        else:
            # create nafheader element and put it in the beginning of
            # the document
            self.kaf_header = etree.Element(self.KAF_HEADER_TAG)
            self.root.insert(0, self.kaf_header)

        if header:
            self.set_header(header)

        text_layer = self.tree.find(self.TEXT_LAYER_TAG)
        if text_layer is not None and len(text_layer):
            self.text = text_layer
        else:
            self.text = etree.SubElement(self.root, self.TEXT_LAYER_TAG)

        terms_layer = self.tree.find(self.TERMS_LAYER_TAG)
        if text_layer is not None and len(terms_layer):
            self.terms = terms_layer
        else:
            self.terms = None

        dependencies_layer = self.tree.find(self.DEPENDENCY_LAYER_TAG)
        if dependencies_layer is not None and len(dependencies_layer):
            self.dependencies = dependencies_layer
        else:
            self.dependencies = None

        chunks_layer = self.tree.find(self.CHUNKS_LAYER_TAG)
        if chunks_layer is not None and len(chunks_layer):
            self.chunks = chunks_layer
        else:
            self.chunks = None

        constituency_layer = self.tree.find(self.CONSTITUENCY_LAYER)
        if constituency_layer is not None and len(constituency_layer):
            self.constituency = constituency_layer
        else:
            self.constituency = None

        named_entities_layer = self.tree.find(self.NAMED_ENTITIES_LAYER_TAG)
        if named_entities_layer is not None and len(named_entities_layer):
            self.entities = named_entities_layer
        else:
            self.entities = None

        coreference_layer = self.tree.find(self.COREFERENCE_LAYER_TAG)
        if coreference_layer is not None and len(coreference_layer):
            self.coreference = coreference_layer
        else:
            self.coreference = None

    def clear_header(self):
        """ Remove the kaf header
        """
        self.root.remove(self.kaf_header)
        self.kaf_header = None

    def set_header(self, kaf_header):
        """ Append headers to the head. If head doesn't exist it is created.

        :param kaf_header: A dict that contains header elements and
        their attributes
        """
        if self.kaf_header:
            for element in kaf_header:
                self.kaf_header.append(element)
            self.kaf_header.attrib.update(kaf_header.attrib)
        else:
            self.kaf_header = kaf_header
            self.root.insert(0, self.kaf_header)

    def add_linguistic_processors(self, layer, name, version, begin_timestamp,
                                  end_timestamp, hostname):
        """Add a Linguistic processor to the head.


        :param layer: Linguistic layer name.
        :param name: Processor name.
        :param version: Processor version.
        :param begin_timestamp: Processing start timestamp
        :param end_timestamp: Processing end timestamp
        :param hostname: name of the procesing machine

        """
        if self.kaf_header is None:
            self.kaf_header = etree.Element(self.KAF_HEADER_TAG)
            self.root.insert(0, self.kaf_header)

        layer_find = self.kaf_header.find("./{0}..[@{1}='{2}']".format(
            self.LINGUISTIC_PROCESSOR_HEAD, self.LAYER_ATTRIBUTE, layer))
        if layer_find:
            layer = layer_find[0]
        else:
            layer = etree.SubElement(
                self.kaf_header, self.LINGUISTIC_PROCESSOR_HEAD, {
                    self.LAYER_ATTRIBUTE: layer})

        etree.SubElement(
            layer, self.LINGUISTIC_PROCESSOR_OCCURRENCE_TAG,
            {self.NAME_ATTRIBUTE: name,
                self.VERSION_ATTRIBUTE: version,
                self.BEGIN_TIMESTAMP_ATTRIBUTE: begin_timestamp,
                self.END_TIMESTAMP_ATTRIBUTE: end_timestamp,
                self.HOSTNAME_ATTRIBUTE: hostname,
             })

    def add_word(self, word, wid, **kwargs):
        """Add a word to the KAF file.
        A word have the next parameters/attributes;
        :param word: The word form
        :param wid: the unique id for the word form.
        :param kwargs: The word optional parameters
            + sent: sentence id of the token (optional)
            + para: paragraph id (optional)
            + offset: the offset of the word form (optional)
            + length: the length of the original word form (optional)
            + page: page id (optional)
        """
        # Prepare the word attributes
        word_attributes = dict(
            (k, v)
            for (k, v) in kwargs.iteritems()
            if k in self.valid_word_attributes)
        word_attributes[self.WORD_ID_ATTRIBUTE] = wid
        # Create a text sub-node for the word and set its attributes
        element = etree.SubElement(
            self.text, self.WORD_OCCURRENCE_TAG, word_attributes)
        element.text = word

    def get_words(self):
        """ Return all the words in the document"""
        return self.text[:]

    def get_words_by_id(self, wid):
        """ Return all the words in the document
        :param wid: WID of the word to retrieve.
        """
        results = self.text.find("{0}[@{1}='{2}']".format(
            self.WORD_OCCURRENCE_TAG, self.WORD_ID_ATTRIBUTE, wid))
        return results and results[0]

    def add_term(self, tid, pos=None, lemma=None, morphofeat=None,
                 term_type=None, words=(), ner=None, external_refs=()):
        """Add a term to the kaf file.
        A Term have the next parameters/attributes:
        :param tid: unique identifier
        :param term_type: type of the term. Currently, 3 values are possible:
                + open: open category term
                + close: close category term
        :param lemma: lemma of the term
        :param pos: part of speech
        :param morphofeat: PennTreebank part of speech tag
        :param words: a list of id of the bounded words.
        :param external_refs: A list of dictionaries that contains the external
         references. Each reference have:
                    + resource
                    + reference
                    + INCOMPLETE
        :param ner: Term NER attribute.
        """
        if self.terms is None:
            self.terms = etree.SubElement(self.root, self.TERMS_LAYER_TAG)

        # TODO Complete external references

        word_attributes = {self.TERM_ID_ATTRIBUTE: tid}
        if pos:
            word_attributes[self.POS_ATTRIBUTE] = pos
        if lemma:
            word_attributes[self.LEMMA_ATTRIBUTE] = lemma
        if term_type:
            word_attributes[self.TYPE_ATTRIBUTE] = term_type
        if morphofeat:
            word_attributes[self.MORPHOFEAT_ATTRIBUTE] = morphofeat
        if ner:
            word_attributes[self.NER_ATTRIBUTE] = ner
        term = etree.SubElement(
            self.terms, self.TERM_OCCURRENCE_TAG, word_attributes)
        if words:
            span = etree.SubElement(term, self.SPAN_TAG)
            for word in words:
                etree.SubElement(
                    span, self.TARGET_TAG, {self.TARGET_ID_ATTRIBUTE: word})
        if external_refs:
            span = etree.SubElement(term, self.EXTERNAL_REFERENCES_TAG)
            for external_ref in external_refs:
                ref_attributes = dict(
                    (k, v)
                    for (k, v) in external_ref.iteritems()
                    if k in self.valid_externalRef_attributes)
                keys = ref_attributes.keys()
                for attribute in self.valid_externalRef_attributes:
                    if attribute not in keys:
                        raise Exception(
                            "External resource not have {0}".format(attribute))
                etree.SubElement(
                    span, self.EXTERNAL_REFERENCE_OCCURRENCE_TAG,
                    ref_attributes)
        return term

    def get_terms(self):
        """ Return all the words in the document"""
        return self.root.findall(
            "{0}/{1}".format(self.TERMS_LAYER_TAG, self.TERM_OCCURRENCE_TAG))

    def get_terms_words(self, term):
        """ Get the words that forms the term.
        :param term: Term node whose words are wanted.

        """
        return term.findall(
            "{0}/{1}".format(self.SPAN_TAG, self.TARGET_TAG))

    def get_terms_references(self, term):
        """ Get references of a term.
        :param term: the term whose references are wanted.

        """
        return term.findall(
            "{0}/{1}".format(
                self.EXTERNAL_REFERENCES_TAG,
                self.EXTERNAL_REFERENCE_OCCURRENCE_TAG))

    def add_dependency(self, origen, to, rfunc):
        """Add a new dependency relation in the text.
        The dependency have the next parameters/attributes:
        :param origen: term id of the source element
        :param to: term id of the target element
        :param rfunc: relational function. One of:
                - mod: indicates the word introducing the dependent in a
                head- modifier relation.
                - subj: indicates the subject in the grammatical relation
                Subject-Predicate.
                - csubj, xsubj, ncsubj: The Grammatical Relations (RL)
                csubj and xsubj may be used for clausal subjects, controlled
                from within, or without,  respectively.
                ncsubj is a non-clausal subject.
                - dobj: Indicates the object in the grammatical relation between
                 a predicate and its direct object.
                - iobj: The relation between a predicate and a non-clausal
                complement introduced by a preposition; type indicates the
                preposition introducing the dependent.
                - obj2: The relation between a predicate and the second
                non-clausal complement in ditransitive constructions.
        """
        if not self.dependencies:
            self.dependencies = etree.SubElement(
                self.root, self.DEPENDENCY_LAYER_TAG)

        dependency_attributes = {
            self.DEPENDENCY_FROM_ATTRIBUTE: origen,
            self.DEPENDENCY_TO_ATTRIBUTE: to,
            self.DEPENDENCY_FUNCTION_ATTRIBUTE: rfunc}
        return etree.SubElement(
            self.dependencies, self.DEPENDENCY_OCCURRENCE_TAG,
            dependency_attributes)

    def get_dependencies(self):
        """Return all the words in the document"""
        return self.root.findall(
            "{0}/{1}".format(
                self.DEPENDENCY_LAYER_TAG, self.DEPENDENCY_OCCURRENCE_TAG))

    def add_chunk(self, cid, head, phrase, case=None, terms=()):
        """"Add a chunk to the kaf document.
        Chunks are noun or prepositional phrases, spanning terms.

        :param cid: unique identifier
        :param head: the chunk head's term id
        :param phrase: typo of the phrase.Valid values:
                        - NP: noun phrase
                        - VP: verbal phrase
                        - PP: prepositional phrase
                        - S: sentence
                        - O: other
        :param case: (optional): declension case
        :param terms: terms that form the chunk.
        """
        # Secure the root
        if not self.chunks:
            self.chunks = etree.SubElement(self.root, self.CHUNKS_LAYER_TAG)
            # Prepare the attributes
        chunk_attributes = {
            self.CHUNK_ID_ATTRIBUTE: cid,
            self.CHUNK_HEAD_ATTRIBUTE: head,
            self.CHUNK_PHRASE_ATTRIBUTE: phrase}
        if case:
            chunk_attributes[self.CHUNK_CASE_ATTRIBUTE] = case
            # Create , and attach, the chunk
        chunk = etree.SubElement(
            self.chunks, self.CHUNK_OCCURRENCE_TAG, chunk_attributes)
        # Add the span terms
        if terms:
            spans = etree.SubElement(chunk, self.SPAN_TAG)
            for term in terms:
                etree.SubElement(
                    spans, self.TARGET_TAG, {self.TARGET_ID_ATTRIBUTE: term})
        return chunk

    def get_chunks(self):
        """Return all the chunks of the text"""
        return self.root.findall(
            "{0}/{1}".format(
                self.DEPENDENCY_LAYER_TAG, self.DEPENDENCY_OCCURRENCE_TAG))

    def get_chunk_terms(self, chunk):
        """Return all the terms of a chunk.
        :param chunk: The chunk node whose terms are wanted"""
        return chunk.findall(
            "{0}/{1}".format(self.SPAN_TAG, self.TARGET_TAG))

    def get_constituency_trees(self):
        """Return all the constituency trees in the document"""
        return self.root.findall(
            "{0}/{1}".format(
                self.CONSTITUENCY_LAYER, self.CONSTITUENCY_TREE_TAG))

    def get_constituent_tree_non_terminals(self, tree):
        """Get all the non terminal constituents of the tree.
        :param tree: The tree whose elements are wanted.
        """
        return tree.findall(self.CONSTITUENCY_NON_TERMINALS)

    def get_constituent_tree_terminals(self, tree):
        """Get all the terminal constituents of the tree.
        :param tree: The tree whose elements are wanted.
        """
        return tree.findall(self.CONSTITUENCY_TERMINALS)

    def get_constituent_tree_edges(self, tree):
        """Get all the edges of the tree.
        :param tree: The tree whose elements are wanted.
        """
        return tree.findall(self.CONSTITUENCY_EDGES)

    def get_constituent_terminal_words(self, constituent):
        """Return all the terms of a terminal constituent.
        :param constituent: The constituent whose terminal words are wanted.
        """
        return constituent.findall(
            "{0}/{1}".format(self.SPAN_TAG, self.TARGET_TAG))

    def add_constituency_tree(self, no_terminals, terminals, edges):
        """ Create and attach the tree to the document and include al
        no-terminals, terminals and edges that conforms the tree.

        :param no_terminals: no terminal tuples:
        (constituent_id, constituent_Label)
        :param terminals: Terminal tuples:
        (constituent_id, [term_id])
        :param edges:  Edge tuples:
        (edge_id, form_id,to_id, head) head is optional(default = false)
        """
        if self.constituency is None:
            self.constituency = etree.SubElement(
                self.root, self.CONSTITUENCY_LAYER)

        tree = etree.SubElement(
            self.constituency, self.CONSTITUENCY_TREE_TAG)

        for no_terminal in no_terminals:
            etree.SubElement(
                tree, self.CONSTITUENCY_NON_TERMINALS, {
                    self.CONSTITUENCY_ID_ATTRIBUTE: no_terminal[0],
                    self.CONSTITUENCY_LABEL_ATTRIBUTE: no_terminal[1]
                })

        for terminal in terminals:
            terminal_node = etree.SubElement(
                tree, self.CONSTITUENCY_TERMINALS, {
                    self.CONSTITUENCY_ID_ATTRIBUTE: terminal[0]})
            span_node = etree.SubElement(terminal_node, self.SPAN_TAG)
            for term in terminal[1]:
                etree.SubElement(span_node, self.TARGET_TAG, {
                    self.TARGET_ID_ATTRIBUTE: term
                })

        for edge in edges:
            edge = etree.SubElement(tree, self.CONSTITUENCY_EDGES, {
                self.CONSTITUENCY_EDGE_ID_ATTRIBUTE: edge[0],
                self.CONSTITUENCY_EDGE_FORM_ATTRIBUTE: edge[1],
                self.CONSTITUENCY_EDGE_TO_ATTRIBUTE: edge[2]
            })
            if len(edge) > 3:
                edge[self.CHUNK_HEAD_ATTRIBUTE] = edge[3]
        return tree

    def add_entity(self, eid, entity_type, references=()):
        """ Add a entity in the document.

        :param eid: The identification code of the entity.
        :param references: The references (ids of the terms) contained in the
        entity.
        :param entity_type: The type of the entity.
        """

        if self.entities is None:
            self.entities = etree.SubElement(
                self.root, self.NAMED_ENTITIES_LAYER_TAG)

        entity_attributes = {self.NAMED_ENTITY_ID_ATTRIBUTE: eid}
        if entity_type:
            entity_attributes[self.NAMED_ENTITY_TYPE_ATTRIBUTE] = entity_type
        entity = etree.SubElement(
            self.entities, self.NAMED_ENTITY_OCCURRENCE_TAG, entity_attributes)
        references_tag = etree.SubElement(entity, "references")
        if references:
            for reference in references:
                span = etree.SubElement(
                    references_tag, self.SPAN_TAG)
                for token in reference:
                    etree.SubElement(
                        span, self.TARGET_TAG, {
                            self.TARGET_ID_ATTRIBUTE: token
                        })
        return entity

    def get_entities(self):
        """Return all the Named Entities in the document"""
        return self.root.findall(
            "{0}/{1}".format(
                self.NAMED_ENTITIES_LAYER_TAG,
                self.NAMED_ENTITY_OCCURRENCE_TAG))

    def get_entity_references(self, named_entity):
        """Return all the terms of a  Named Entities in the document.
        :param named_entity: The entity whose references are wanted."""
        return named_entity.findall(
            "{0}/{1}".format(
                self.NAMED_ENTITY_REFERENCES_GROUP_TAG, self.SPAN_TAG))

    def add_coreference(self, coid, references=(), forms=None):
        """ Add a coreference cluster to the document.
        :param coid: The identification code of the cluster.
        :param references: The references contained in the cluster
        :param forms: The forms of the coreference mentions

        """
        if self.coreference is None:
            self.coreference = etree.SubElement(
                self.root, self.COREFERENCE_LAYER_TAG)

        coref_attrib = {self.COREFERENCE_ID_ATTRIBUTE: coid}
        entity = etree.SubElement(
            self.coreference, self.COREFERENCE_OCCURRENCE_TAG, coref_attrib)
        if forms:
            forms = iter(forms)
        if references:
            for reference in references:
                if forms:
                    form = forms.next()
                    comment = etree.Comment(
                        form.decode("utf-8").replace("-", " - "))
                    entity.append(comment)
                span = etree.SubElement(entity, self.SPAN_TAG)
                for token in reference:
                    etree.SubElement(
                        span, self.TARGET_TAG, {
                            self.TARGET_ID_ATTRIBUTE: token})
        return entity

    def get_coreference(self):
        """Return all the coreference entity in the document"""
        return self.root.findall(
            "{0}/{1}".format(
                self.COREFERENCE_LAYER_TAG,
                self.COREFERENCE_OCCURRENCE_TAG))

    def get_coreference_mentions(self, named_entity):
        """Return all the terms of a  Named Entities in the document.
        :param named_entity: The entity whose references are wanted."""
        return named_entity.findall("{0}".format(self.SPAN_TAG))

    def get_reference_span(self, reference):
        """Return all the terms of a reference in the document.

        :param reference: The reference node whose terms are wanted."""
        return reference.findall(self.TARGET_TAG)

    def _indent(self, elem, level=0):
        """ Include indentation in the output making it more human readable.

        :param elem: Element to indent.
        :param level: Level of indentation.
        """
        i = "\n" + level * "  "
        child = None
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for child in elem:
                self._indent(child, level+1)
            # This seeks for the las child processed in for, is not a code
            # indentation error
            if child is not None and (not child.tail) or (not child.tail.strip()):
                child.tail = i
        else:
            if level is not None and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def validateExternalDTD(self, source):
        """  Validate the current NAF document against the DTD.
        :param source: The DTD source
        :return True or False
        """
        self.dtd = etree.DTD(source)
        return self.dtd.validate(self.root)

    def write(self, output, encoding):
        """Write document into a file.
        :param output: The output target for the document. May be a file type
         object or a file name.
        :param encoding: The encoding of the output.
        """
        self._indent(self.root)
        output.write(etree.tostring(self.root, encoding=encoding,))

    def __str__(self):
        self._indent(self.root)
        return etree.tostring(self.root, encoding=self.encoding)


class KAFDocument(NAFDocument):
    KAF_TAG = "KAF"
    LANGUAGE_ATTRIBUTE = "{http://www.w3.org/XML/1998/namespace}lang"
    VERSION_ATTRIBUTE = "version"
    NS = {}

    # Head
    KAF_HEADER_TAG = "kafHeader"
    NAME_ATTRIBUTE = "name"
    LINGUISTIC_PROCESSOR_HEAD = "linguisticProcessors"
    LAYER_ATTRIBUTE = "layer"
    LINGUISTIC_PROCESSOR_OCCURRENCE_TAG = "lp"
    TIMESTAMP_ATTRIBUTE = "timestamp"

    # Text layer
    TEXT_LAYER_TAG = "text"
    WORD_OCCURRENCE_TAG = "wf"
    WORD_ID_ATTRIBUTE = "wid"

    # Term layer
    TERMS_LAYER_TAG = "terms"
    TERM_OCCURRENCE_TAG = "term"
    TERM_ID_ATTRIBUTE = "tid"
    NER_ATTRIBUTE = "ner"
    TYPE_ATTRIBUTE = "type"
    LEMMA_ATTRIBUTE = "lemma"
    POS_ATTRIBUTE = "pos"
    MORPHOFEAT_ATTRIBUTE = "morphofeat"

    # Chunking layer
    CHUNKS_LAYER_TAG = "chunks"
    CHUNK_OCCURRENCE_TAG = "chunk"
    CHUNK_CASE_ATTRIBUTE = "case"
    CHUNK_PHRASE_ATTRIBUTE = "phrase"
    CHUNK_HEAD_ATTRIBUTE = "head"
    CHUNK_ID_ATTRIBUTE = "cid"

    # Constituency Layer
    CONSTITUENCY_LAYER = "constituency"
    CONSTITUENCY_TREE_TAG = "tree"
    CONSTITUENCY_ID_ATTRIBUTE = "id"
    CONSTITUENCY_LABEL_ATTRIBUTE = "label"
    CONSTITUENCY_NON_TERMINALS = "nt"
    CONSTITUENCY_TERMINALS = "t"
    CONSTITUENCY_EDGES = "edge"
    CONSTITUENCY_EDGE_ID_ATTRIBUTE = "id"
    CONSTITUENCY_EDGE_FORM_ATTRIBUTE = "from"
    CONSTITUENCY_EDGE_TO_ATTRIBUTE = "to"

    # Dependency Layer
    DEPENDENCY_LAYER_TAG = "deps"
    DEPENDENCY_OCCURRENCE_TAG = "dep"
    DEPENDENCY_FROM_ATTRIBUTE = "from"
    DEPENDENCY_FUNCTION_ATTRIBUTE = "rfunc"
    DEPENDENCY_TO_ATTRIBUTE = "to"

    # Coreference Layer
    COREFERENCE_LAYER_TAG = "coreferences"
    COREFERENCE_ID_ATTRIBUTE = "coid"
    COREFERENCE_OCCURRENCE_TAG = "coref"

    # Name Entity layer
    NAMED_ENTITIES_LAYER_TAG = "entities"
    NAMED_ENTITY_OCCURRENCE_TAG = "entity"
    NAMED_ENTITY_ID_ATTRIBUTE = "eid"
    NAMED_ENTITY_TYPE_ATTRIBUTE = "type"
    NAMED_ENTITY_REFERENCES_GROUP_TAG = "references"

    # References tags
    SPAN_TAG = "span"
    TARGET_ID_ATTRIBUTE = "id"
    TARGET_TAG = "target"

    # External references
    EXTERNAL_REFERENCE_OCCURRENCE_TAG = "externalRef"
    EXTERNAL_REFERENCES_TAG = "externalReferences"
