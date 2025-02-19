import pandas as pd

class parseData():
    def __init__(self, raw_data):
        self.raw_data = raw_data
    
    def parse_attendance_data(raw_data):
        # Split the data into lines
        lines = raw_data.strip().split('\n')
        
        # Skip the first line ("List of Attendance")
        data_lines = lines[2:]  # Start from the actual data rows
        
        # Initialize lists to store the parsed data
        parsed_data = []
        
        for line in data_lines:
            # Split the line by spaces, but keep quoted strings together
            parts = line.split()
            
            # Extract components
            sno = parts[0]
            
            # Find course code and name
            course_info = ' '.join(parts[1:parts.index('Approved')]).split(' : ')
            course_code = course_info[0]
            course_name = course_info[1]
            
            # Get remaining fields
            remaining = parts[parts.index('Approved'):]
            status = remaining[0]
            type_field = remaining[1]
            section = remaining[2]
            batch = remaining[3]
            
            # Handle the attendance numbers
            # If there are no numbers (last two rows), fill with zeros
            if len(remaining) > 4:
                present = remaining[4]
                absent = remaining[5] if len(remaining) > 5 else '0'
                total = remaining[6] if len(remaining) > 6 else '0'
                attendance_pct = remaining[7] if len(remaining) > 7 else '0'
            else:
                present = '0'
                absent = '0'
                total = '0'
                attendance_pct = '0'
            
            # Create a row of data
            row = [
                sno,
                course_code,
                course_name,
                status,
                type_field,
                section,
                batch,
                present,
                absent,
                total,
                attendance_pct
            ]
            
            parsed_data.append(row)
        
        # Create DataFrame
        columns = [
            'S.No.',
            'Course Code',
            'Course Name',
            'Status',
            'Type',
            'Section',
            'Batch',
            'Present',
            'Absent',
            'Total',
            'Attendance %'
        ]
        
        df = pd.DataFrame(parsed_data, columns=columns)
        df.to_csv('attendance_data.csv', index=False)

        return df