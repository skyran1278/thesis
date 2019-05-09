' @license Version v2.4.0
' Version.vb
'
' Copyright (c) 2016-present, skyran
'
' This source code is licensed under the MIT license found in the
' LICENSE file in the root directory of this source tree.


' 隨工作簿不同而需更改的參數:
' VERSION_URL: 該工作簿 version.txt
' DOWNLOAD_URL: 該工作簿 下載檔案位置
Private Const DOWNLOAD_URL = "https://github.com/skyran1278/VbaProject/raw/master/20180126_SmartCut/VBA/SmartCut.xlsm"
Private Const VERSION_URL = "https://github.com/skyran1278/VbaProject/raw/master/20180126_SmartCut/VBA/Version.txt"

Sub VerifyPassword()
'
' 驗證密碼.
'
' @since 1.0.0
'

    Dim srvXmlHttp As Object
    Dim inputPwd As String
    Dim cloudPwd As String
    Dim passwordUrl As String

    ' passwordUrl: pwd.txt
    passwordUrl = "https://github.com/skyran1278/VbaProject/raw/master/utils/pwd.txt"

    Set srvXmlHttp = CreateObject("MSXML2.serverXMLHTTP")

    srvXmlHttp.Open "GET", passwordUrl, False

    inputPwd = Trim(Application.InputBox("Please Input Passward.", "Verify User Identity", Type:=2))

    srvXmlHttp.send

    cloudPwd = srvXmlHttp.ResponseText

    ' 消除空白行
    cloudPwd = Trim(Replace(cloudPwd, Chr(10), ""))

    If inputPwd <> cloudPwd Then

        MsgBox "Wrong Password"
        ThisWorkbook.Close SaveChanges:=False

    End If

End Sub


Sub CheckVersion()
'
' 驗證版本號.
'
' @since 1.0.0
'

    ' 此程序包含的變數
    Dim srvXmlHttp As Object
    Dim shell As Object
    Dim ws_version As Worksheet
    Dim currentVersion As String
    Dim latestVersion As String
    Dim releaseNotes As String

    Set srvXmlHttp = CreateObject("MSXML2.serverXMLHTTP")

    Set ws_version = ThisWorkbook.Worksheets("Release Notes")

    srvXmlHttp.Open "GET", VERSION_URL, False

    srvXmlHttp.send

    latestVersionAndReleaseNotes = srvXmlHttp.ResponseText

    currentVersion = ws_version.Cells(3, 3)

    ' 區分版本號和更新說明
    latestVersionAndReleaseNotes = Split(latestVersionAndReleaseNotes, Chr(10) & "===" & Chr(10))
    latestVersion = latestVersionAndReleaseNotes(0)
    releaseNotes = latestVersionAndReleaseNotes(1)

    If CompareVersion(currentVersion, latestVersion) Then

        If MsgBox(releaseNotes, vbYesNo, "Download Latest Version From Browser") = vbYes Then

            Set shell = CreateObject("Wscript.Shell")
            shell.Run (DOWNLOAD_URL)
            MsgBox "Please close this file and use new file from browser.", vbOKOnly

        End If

    End If

End Sub


Private Function CompareVersion(currentVersion As String, latestVersion As String)
'
' compare which version is latest.
'
' @since 1.0.0
' @param {string} [currentVersion] currentVersion.
' @param {string} [latestVersion] latestVersion.
' @return {boolean} [CompareVersion] latestVersion > currentVersion return true.
'

    arrCurrentVersion = Split(currentVersion, ".")
    arrLatestVersion = Split(latestVersion, ".")

    If arrLatestVersion(0) > arrCurrentVersion(0) Then
        CompareVersion = True

    ElseIf arrLatestVersion(1) > arrCurrentVersion(1) Then
        CompareVersion = True

    ElseIf arrLatestVersion(2) > arrCurrentVersion(2) Then
        CompareVersion = True

    Else
        CompareVersion = False

    End If

End Function


Private Sub Workbook_Open()
'
' * 目的: 驗證密碼，檢查程式最新版本，並自動提示更新
'
' * 隨工作簿不同而需更改的參數:
'       VERSION_URL: 該工作簿 version.txt
'       DOWNLOAD_URL: 該工作簿 下載檔案位置
'
' * 重要且通常不會更動數值:
'       工作表位置: 版本資訊
'       名稱: Cells(2, 3)
'       目前版本號: Cells(3, 3)
'       最新版本號: Cells(4, 3)
'
' * 測試環境:
'       office 2016 in windows 10
'       Mac 版本容易出現錯誤，不推薦在 Mac 執行

    ' Dim ws_version As Worksheet
    ' Set ws_version = ThisWorkbook.Worksheets("Release Notes")

    On Error GoTo ErrorHandler

    Call VerifyPassword
    Call CheckVersion

    Exit Sub

ErrorHandler:
    MsgBox(Err.Description)

    inputPwd = Trim(Application.InputBox("Please Input Strong Passward.", "No Internet Connect", Type:=2))

    strongPwd = "28862952"

    If inputPwd <> strongPwd Then

        MsgBox "Wrong Password"
        ThisWorkbook.Close SaveChanges:=False

    End If

    ' ws_version.Cells.Font.Name = "微軟正黑體"
    ' ws_version.Cells.Font.Name = "Calibri"

End Sub


