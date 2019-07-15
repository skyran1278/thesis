Sub 巨集1()
'
' 巨集1 巨集
'
' 快速鍵: Ctrl+e
'

    Sheets("傳統斷筋").Select
    Columns("W:X").Select
    Selection.Copy
    Sheets("多點斷筋").Select
    Columns("Y:Y").Select
    ActiveSheet.Paste
    Application.WindowState = xlNormal
    Windows("20190506 103622 SmartCut 效益.xlsx").Activate
    Application.CutCopyMode = False
    Selection.Copy
    Workbooks(Workbooks.Count).Activate
    Columns("AA:AA").Select
    ActiveSheet.Paste
    ActiveWindow.ScrollColumn = 13
End Sub
