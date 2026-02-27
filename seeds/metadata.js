const german_noun_metadata = {
  morphology: {
    gender: 'die',
    plural: 'Erinnerungen',
    genitive: 'Erinnerung',
  },
  grammar_profile: {
    direct_valency: [],
    prepositional_valency: [
      {
        preposition: 'an',
        required_case: 'AKK',
        context_hint: 'the memory of what',
      },
    ],
  },
};

const german_verb_metadata = {
  morphology: {
    aux_verb: 'haben',
    is_regular: true,
    partizip_ii: 'erinnert',
    conjugation: {
      present: ['erinnere', 'erinnerst', 'erinnert', 'erinnern', 'erinnert', 'erinnern'],
      past: [
        'erinnerte',
        'erinnertest',
        'erinnerte',
        'erinnerten',
        'erinnertet',
        'erinnerten',
      ],
    },
  },
  grammar_profile: {
    reflexive_case: 'AKK',
    direct_valency: [],
    prepositional_valency: [
      {
        preposition: 'bei',
        required_case: 'DAT',
        context_hint: 'the person',
      },
      {
        preposition: 'über',
        required_case: 'AKK',
        context_hint: 'the topic',
      },
    ],
  },
};

const german_adjective_metadata = {
  morphology: {
    comparative: 'schöner',
    superlative: 'am schönsten',
    is_irregular: false,
  },
  grammar_profile: {
    direct_valency: [],
    prepositional_valency: [
      {
        preposition: 'auf',
        required_case: 'AKK',
        context_hint: 'the object of pride',
      },
    ],
  },
};
