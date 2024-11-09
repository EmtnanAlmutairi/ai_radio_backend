<?php
// تعيين نوع المحتوى إلى JSON
header('Content-Type: application/json'); 

// اسم المجلد الذي ستخزن فيه الملفات
$uploadDir = 'uploads/';  // قم بتعديل المسار حسب احتياجك

// التأكد من أن المجلد موجود وإذا لم يكن موجودًا، يتم إنشاؤه
if (!file_exists($uploadDir)) {
    mkdir($uploadDir, 0777, true);
}

// التحقق إذا كانت البيانات تم إرسالها باستخدام POST
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // التحقق إذا كان الملف قد تم إرساله بنجاح
    if (isset($_FILES['file']) && $_FILES['file']['error'] == UPLOAD_ERR_OK) {
        // تحديد اسم الملف الجديد
        $fileTmpPath = $_FILES['file']['tmp_name'];
        $fileName = $_FILES['file']['name'];
        $fileSize = $_FILES['file']['size'];
        $fileType = $_FILES['file']['type'];

        // تحديد امتداد الملف (يجب التأكد من نوع الملف)
        $fileExtension = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

        // تحديد مسار حفظ الملف
        $newFileName = uniqid() . '.' . $fileExtension;  // استخدام اسم فريد لتجنب الكتابة على الملفات القديمة
        $uploadFilePath = $uploadDir . $newFileName;

        // التحقق من نوع الملف للتأكد من أنه ملف صوتي
        if ($fileType === 'audio/mpeg') {
            // نقل الملف إلى المجلد المحدد
            if (move_uploaded_file($fileTmpPath, $uploadFilePath)) {
                // إعادة رابط الملف المرفوع
                $fileUrl = 'https://radioallam.devadnan.net/uploads/' . $newFileName; // تعديل المسار حسب احتياجك

                // إرسال الاستجابة بصيغة JSON تحتوي على رابط الملف
                echo json_encode(['file_url' => $fileUrl]);
            } else {
                echo json_encode(['error' => 'فشل في رفع الملف.']);
            }
        } else {
            echo json_encode(['error' => 'الملف المرفوع ليس من نوع mp3.']);
        }
    } else {
        echo json_encode(['error' => 'لم يتم إرسال الملف أو حدث خطأ في الرفع.']);
    }
} else {
    echo json_encode(['error' => 'يرجى إرسال الملف عبر طلب POST.']);
}
?>
