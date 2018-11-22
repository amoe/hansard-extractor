def transform_csv(records):
    result = []

    for rec in records:
        new_record = rec.copy()
        new_record['member_contribution'] = ' '.join(rec['member_contribution'])
        result.append(new_record)

    return result

        
            
