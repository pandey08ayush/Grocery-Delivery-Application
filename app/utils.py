def write_single_csv_data(writer, headers, queryset, fields):
    # Write the headers
    writer.writerow(headers)

    # Write the data rows
    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        writer.writerow(row)