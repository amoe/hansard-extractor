def transform_csv(records):
    result = []

    for rec in records:
        sentences = rec['member_contribution']
        
        for index, sentence in enumerate(sentences):
            new_record = rec.copy()
            del new_record['member_contribution']
            new_record['sentence_index'] = index
            new_record['content'] = sentence
            result.append(new_record)

    return result

        
            
