import pandas as pd 

#--------------------------------------------------
# HELPER FUNCTIONS: Build a DataFrame from user input
#--------------------------------------------------

def get_dataframe(df_name,columns):
    """ Columns: list of columns names to collect for this dataset """

    print(f"\n---Enter data for {df_name} (columns:{columns})---")
    num_rows = int(input(f"How many rows for {df_name}? "))

    data = {col:[]for col in columns}
    for r in range(num_rows):
        print(f"\nRow {r+1}:")
        for col in columns:
            value = input(f" {col}:").strip()
        if value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                pass # keep as string
        data[col].append(value)

        df = pd.DataFrame(data)
        print(f"\n{df_name}:\n{df}")
        return df

    #--------------------------------------------------
    # 1.CREATE DATAFRAMES FROM USER INPUT
    #--------------------------------------------------

    print("="*60)
    print("STEP 1: Build Dataset 1 - Student basic info")
    print("="*60)
    student_df1 = get_dataframe("Dataset 1(Students)",["StudentID","Name","Branch"])

    print("="*60)
    print("STEP 2: Build Dataset 2 - Student marks")
    print("="*60)
    marks_df2 = get_dataframe("Dataset 2(Marks)",["StudentID","Marks"])

    #--------------------------------------------------
    # 2. CONCATINATION
    #--------------------------------------------------

    # VERTICAL concatenation (stacking rows)- combing two batches
    combined_students = pd.concate([student_df1,marks_df2], axis=0, ignore_index=True)
    print("Vertical Concatenation (axis=0):\n",combined_students,"\n")

    #Horizontal Concatenation (stacking columns side-by-side)
    print("---Enter extra colmn data to horizontally concatenate with Dataset 1---")
    n_rows_extra = len(student_df1)
    print(f"Must match Dataset 1's row count :{n_rows_extra})")
    attendance_values = []
    for r in range(n_rows_extra):
        val = input(f"Attendance(%) for row {r+1}:").strip()
        attendance_values.append(int(val)if val.isdigit()else val)

    extra_df = pd.DataFrame({"Attendance(%)":attendance_values})
    Horizontal_concat = pd.concat([student_df1,extra_df], axis=1)
    print("Horizontal Concatenation (axis=1):\n",Horizontal_concat,"\n")


    #--------------------------------------------------
    # 3. MERGING(SQL-style join based on common key)
    #--------------------------------------------------

    inner_merged = pd.merge(student_df1,marks_df2, on="StudentID", how="inner")
    print("Inner Merge:\n", inner_merged,"\n")

    left_merged = pd.merge(student_df1,marks_df2, on="StudentID", how="left")
    print("Left Merge:\n", left_merged,"\n")

    right_merged = pd.merge(student_df1,marks_df2, on="StudentID", how="right")
    print("Right Merge:\n", right_merged,"\n")

    outer_merged = pd.merge(student_df1,marks_df2, on="StudentID", how="outer")
    print("Outer Merge:\n", outer_merged,"\n")

    #--------------------------------------------------
    # 4. join method (Join on index instead of column)
    #--------------------------------------------------

    df_a = student_df1.set_index("StudentID")
    df_b = marks_df2.set_index("StudentID")

    joined_df = df_a.join(df_b, how="inner")
    print("Join (index-based,inner):\n",joined_df,"\n")

    joined_outer_df = df_a.join(df_b, how="outer")
    print("Join (index-based,outer):\n",joined_outer_df,"\n")

    #--------------------------------------------------
    # 5. Merge with Different column names 
    #--------------------------------------------------

    marks_df_renamed = marks_df2.rename(columns={"StudentID":"ID"})
    merged_diff_cols = pd.merge(
        student_df1,marks_df_renamed, 
        left_on="StudentID", right_on="ID",
          how="inner").drop(columns=["ID"])
    print("Merge with different column names:\n",merged_diff_cols,"\n")

    #--------------------------------------------------
    # 6. Merge on Multiple keys
    #--------------------------------------------------

    print("="*60)
    print("STEP 4: build Dataset X - student per semester")
    print("="*60)
    df_y = get_dataframe("Dataset X(Grades)",["StudentID","Semester","Grade"])

    merge_multi_key = pd.merge(student_df1,df_y, on=["StudentID","Semester"], how="inner")
    print("Merge on multiple keys:\n",merge_multi_key,"\n")